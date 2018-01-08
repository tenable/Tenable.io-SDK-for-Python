import six
import os
import re
import time

from datetime import datetime, timedelta

from tenable_io.api.models import Scan, ScanSettings, Template
from tenable_io.api.scans import ScansApi, ScanCreateRequest, ScanExportRequest, ScanImportRequest, ScanLaunchRequest
from tenable_io.exceptions import TenableIOException
import tenable_io.util as util


class ScanHelper(object):

    STATUSES_STOPPED = [
        Scan.STATUS_ABORTED,
        Scan.STATUS_CANCELED,
        Scan.STATUS_COMPLETED,
        Scan.STATUS_IMPORTED,
        Scan.STATUS_EMPTY,
    ]

    STATUSES_PENDING = [
        Scan.STATUS_INITIALIZING,
        Scan.STATUS_PENDING
    ]

    def __init__(self, client):
        self._client = client

    def scans(self, name_regex=None, name=None, folder_id=None):
        """Get scans.

        :param name: A string to match scans with, default to None. Ignored if the `name_regex` argument is passed.
        :param name_regex: A regular expression to match scans' names with, default to None.
        :param folder_id: Only scans in the folder identified by `folder_id`, default to None.
        :return: A list of ScanRef.
        """
        scans = self._client.scans_api.list(folder_id=folder_id).scans
        if name_regex:
            name_regex = re.compile(name_regex)
            scans = [scan for scan in scans if name_regex.match(scan.name)]
        elif name:
            scans = [scan for scan in scans if name == scan.name]
        return [ScanRef(self._client, scan.id) for scan in scans]

    def id(self, id):
        """Get scan by ID.

        :param id: Scan ID.
        :return: ScanRef referenced by id if exists.
        """
        self._client.scans_api.details(id)
        # object_id is not returned by the API when the current user is not the owner of the scan.
        # return ScanRef(self._client, self._client.scans_api.details(id).info.object_id)
        return ScanRef(self._client, id)

    def stop_all(self, folder=None, folder_id=None):
        """Stop all scans.

        :param folder: Instance of FolderRef. Stop all scan in the folder only. Default to None.
        :param folder_id: Stop all scan in the folder identified by folder_id only. Default to None.
        :return: The current instance of ScanHelper.
        """
        from tenable_io.helpers.folder import FolderRef
        if folder_id is None and isinstance(folder, FolderRef):
            folder_id = folder.id

        scans = self.scans(folder_id=folder_id)
        for scan in scans:
            try:
                # Send stop requests for all scans first before waiting for it to be fully stopped.
                scan.stop(False)
            except TenableIOException:
                pass
        # Wait for scans to stop after all the stop requests are made.
        [scan.wait_until_stopped() for scan in scans]
        return self

    def create(self, name, text_targets, template):
        """Get scan by ID.

        :param name: The name of the Scan to be created.
        :param text_targets: A string of comma separated targets or a list of targets.
        :param template: The name or title of the template, or an instance of Template.
        :return: ScanRef referenced by id if exists.
        """
        if isinstance(text_targets, list):
            text_targets = ','.join(text_targets)

        t = template

        if not isinstance(t, Template):
            t = self.template(name=template)

        if not t:
            t = self.template(title=template)

        if not t:
            raise TenableIOException(u'Template with name or title as "%s" not found.' % template)

        scan_id = self._client.scans_api.create(
            ScanCreateRequest(
                t.uuid,
                ScanSettings(
                    name,
                    text_targets,
                )
            )
        )
        return ScanRef(self._client, scan_id)

    def template(self, name=None, title=None):
        """Get template by name or title. The `title` argument is ignored if `name` is passed.

        :param name: The name of the template.
        :param title: The title of the template.
        :return: An instance of Template if exists, otherwise None.
        """
        template = None

        if name:
            template_list = self._client.editor_api.list('scan')
            for t in template_list.templates:
                if t.name == name:
                    template = t
                    break

        elif title:
            template_list = self._client.editor_api.list('scan')
            for t in template_list.templates:
                if t.title == title:
                    template = t
                    break

        return template

    def import_scan(self, path, include_aggregate=True):
        """Uploads and then imports scan report.

        :param path: Path of the scan report.
        :param include_aggregate: Flag indicating whether import scan results should be shown on Workbenches.
        :return: ScanRef referenced by id if exists.
        """
        uploaded_file_name = self._client.file_helper.upload(path)

        imported_scan_id = self._client.scans_api.import_scan(ScanImportRequest(uploaded_file_name), include_aggregate)

        return self.id(imported_scan_id)

    def activities(
            self,
            targets=None,
            fqdns=None,
            ipv4s=None,
            mac_addresses=None,
            netbios_names=None,
            tenable_uuids=None,
            date_range=7
    ):
        """Get scan activities against a list of targets. Note: For uncompleted scans, only the targets configured for
        the scan are matched against on the SDK-side. Completed scans are queried and matched on the API server-side.

        :param targets: A single string target or a list of string targets in IPv4 or FQDN format.
        :param fqdns: A list of string values in FQDN format.
        :param ipv4s: A list of string values in IPv4 format.
        :param mac_addresses: A list of string values in MAC address format.
        :param netbios_names: A list of netbios_name's.
        :param tenable_uuids: A list of tenable_uuid's.
        :param date_range: The number of days of data prior to and including today that should be considered.
        return: ScanActivity list sort by timestamp; active ScanActivity's are ordered first with None timestamp.
        """
        if not isinstance(targets, list):
            targets = [targets] if targets else []

        if not fqdns:
            fqdns = []
        if not ipv4s:
            ipv4s = []
        if not mac_addresses:
            mac_addresses = []
        if not netbios_names:
            netbios_names = []
        if not tenable_uuids:
            tenable_uuids = []

        for target in targets:
            if util.is_ipv4(target):
                ipv4s.append(target)
            if util.is_mac(target):
                mac_addresses.append(target)
            elif isinstance(target, six.string_types) and len(target) > 0:
                fqdns.append(target)

        asset_activities = self._asset_activities(fqdns, ipv4s, mac_addresses, netbios_names, tenable_uuids, date_range)
        running_activities = self._running_activities(fqdns, ipv4s)

        return running_activities + asset_activities

    def _asset_activities(self, fqdns, ipv4s, mac_addresses, netbios_names, tenable_uuids, date_range):
        """Get scan activities against FQDNs and IPv4s targets from scan are not completed yet. Note: The method is to
        inspect all active scan jobs from all scanners.

        :param fqdns: List of string targets in FQDN-format.
        :param ipv4s: List of string targets in IPv4-format.
        :param date_range: The number of days of data prior to and including today that should be considered.
        return: ScanActivity list.
        """
        activities = []
        filters = []

        for fqdn in fqdns:
            filters.append({
                'quality': 'eq',
                'filter': 'fqdn',
                'value': fqdn
            })

        for ipv4 in ipv4s:
            filters.append({
                'quality': 'eq',
                'filter': 'ipv4',
                'value': ipv4
            })

        for mac_address in mac_addresses:
            filters.append({
                'quality': 'eq',
                'filter': 'mac_address',
                'value': mac_address
            })

        for netbios_name in netbios_names:
            filters.append({
                'quality': 'eq',
                'filter': 'netbios_name',
                'value': netbios_name
            })

        for tenable_uuid in tenable_uuids:
            filters.append({
                'quality': 'eq',
                'filter': 'tenable_uuid',
                'value': tenable_uuid
            })

        if len(filters):
            # Get assets associated with targets
            assets = self._client.workbenches_api.assets(
                date_range=date_range,
                filters=filters,
                filter_search_type='or'
            )

            for asset in assets.assets:
                activity_list = self._client.workbenches_api.asset_activity(asset.id)
                activities.extend([a for a in activity_list.activity if None not in [a.scan_id, a.schedule_id]])

        # TODO support for date_range is broken as of 2017/05/15, remove manual filtering when support is functional.
        # Filter out activities that are outside of the time range.
        start = datetime.now() - timedelta(days=date_range)
        activities = [
            ScanActivity(self._client, None, a.scan_id, None, a.schedule_id, a.timestamp)
            for a in activities
            if a.timestamp and start < datetime.strptime(a.timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
        ]

        # Build scan_id lookup table with schedule_uuid as keys.
        scans = self._client.scans_api.list()
        scan_ids = {
            s.schedule_uuid: s.id
            for s in scans.scans
        }

        # Group activities by scan_id (a scenario where this can be possible is when a scan have multiple targets that
        # matches the targets being queried).
        activities_by_scan_history = {}
        for a in activities:
            if a.schedule_uuid in scan_ids:
                a.scan_id = scan_ids[a.schedule_uuid]
                if a.scan_id not in activities_by_scan_history:
                    activities_by_scan_history[a.scan_id] = {}
                if a.history_uuid not in activities_by_scan_history[a.scan_id]:
                    activities_by_scan_history[a.scan_id][a.history_uuid] = []
                activities_by_scan_history[a.scan_id][a.history_uuid].append(a)

        # Look up history_id for each history_uuid
        for scan_id, activities_by_history_uuid in activities_by_scan_history.items():
            details = self._client.scans_api.details(scan_id)
            for history in details.history:
                if history.uuid in activities_by_history_uuid:
                    for a in activities_by_history_uuid[history.uuid]:
                        a.history_id = history.history_id
                    del activities_by_history_uuid[history.uuid]
                if len(activities_by_history_uuid) < 1:
                    break

        # Order by timestamp
        return sorted(activities, key=lambda a: datetime.strptime(a.timestamp, '%Y-%m-%dT%H:%M:%S.%fZ'), reverse=True)

    def _running_activities(self, fqdns, ipv4s):
        """Get scan activities against FQDNs and IPv4s targets from scan are not completed yet. Note: The method is to
        inspect all active scan jobs from all scanners.

        :param fqdns: List of string targets in FQDN-format.
        :param ipv4s: List of string targets in IPv4-format.
        return: ScanActivity list.
        """
        activities = []

        # Iterate through all scanners with at least 1 running scans.
        for scanner in [s for s in self._client.scanners_api.list().scanners if s.scan_count > 0]:
            scans = self._client.scanners_api.get_scans(scanner.id)
            # Iterate through each running scan.
            for s in scans.scans:
                # Find the corresponding history.
                history = None
                for h in self._client.scans_api.details(scan_id=s.scan_id).history:
                    if s.id == h.uuid:
                        history = h
                        break
                assert history, u'There should be history with the matching ID returned by the scanner.'

                details = self._client.scans_api.details(scan_id=s.scan_id, history_id=history.history_id)

                # Check if this scan has matching targets.
                if details.info.targets:
                    scan_targets = set(details.info.targets.lower().split(u','))
                    if scan_targets.intersection(fqdns) or scan_targets.intersection(ipv4s):
                        activities.append(
                            ScanActivity(
                                self._client,
                                history.history_id,
                                history.uuid,
                                s.scan_id,
                                details.info.schedule_uuid
                            )
                        )

        return sorted(activities, key=lambda o: o.scan_id, reverse=True)


class ScanActivity(object):

    def __init__(
            self,
            client=None,
            history_id=None,
            history_uuid=None,
            scan_id=None,
            schedule_uuid=None,
            timestamp=None,
    ):
        self._client = client
        self.history_id = history_id
        self.history_uuid = history_uuid
        self.scan_id = scan_id
        self.schedule_uuid = schedule_uuid
        self.timestamp = timestamp

    def scan(self):
        return None if self.scan_id is None else ScanRef(self._client, self.scan_id)

    def details(self):
        return None if self.scan_id is None else \
            self._client.scans_api.details(scan_id=self.scan_id, history_id=self.history_id)


class ScanRef(object):

    def __init__(self, client, id):
        self._client = client
        self.id = id

    def copy(self):
        """Create a copy of the scan.

        :return: An instance of ScanRef that references the newly copied scan.
        """
        scan = self._client.scans_api.copy(self.id)
        return ScanRef(self._client, scan.id)

    def delete(self, force_stop=False):
        """Delete the scan.

        :return: The same ScanRef instance.
        """
        if force_stop and not self.stopped():
            self.stop()
        self._client.scans_api.delete(self.id)
        return self

    def details(self, history_id=None):
        """Get the scan detail.

        :return: An instance of :class:`tenable_io.api.models.ScanDetails`.
        """
        return self._client.scans_api.details(self.id, history_id=history_id)

    def download(self, path, history_id=None, format=ScanExportRequest.FORMAT_PDF,
                 chapter=ScanExportRequest.CHAPTER_EXECUTIVE_SUMMARY, file_open_mode='wb'):
        """Download a scan report.

        :param path: The file path to save the report to.
        :param format: The report format. Default to :class:`tenable_io.api.scans.ScanExportRequest`.FORMAT_PDF.
        :param chapter: The report contents. Default to \
        :class:`tenable_io.api.scans.ScanExportRequest`.CHAPTER_EXECUTIVE_SUMMARY.
        :param file_open_mode: The open mode to the file output. Default to "wb".
        :param history_id: A specific scan history ID, None for the most recent scan history. default to None.
        :return: The same ScanRef instance.
        """
        self.wait_until_stopped(history_id=history_id)

        if format in [ScanExportRequest.FORMAT_HTML, ScanExportRequest.FORMAT_PDF]:
            export_request = ScanExportRequest(format=format, chapters=chapter)
        else:
            export_request = ScanExportRequest(format=format)

        file_id = self._client.scans_api.export_request(
            self.id,
            export_request,
            history_id
        )
        util.wait_until(
            lambda: self._client.scans_api.export_status(self.id, file_id) == ScansApi.STATUS_EXPORT_READY)

        iter_content = self._client.scans_api.export_download(self.id, file_id)
        with open(path, file_open_mode) as fd:
            for chunk in iter_content:
                fd.write(chunk)
        return self

    def histories(self, since=None):
        """Get scan histories.

        :param since: As instance of `datetime`. Default to None. \
        If defined, only scan histories after this are returned.
        :return: A list of :class:`tenable_io.api.models.ScanDetailsHistory`.
        """
        histories = self.details().history
        if since:
            assert isinstance(since, datetime), '`since` parameter should be an instance of datetime.'
            ts = time.mktime(since.timetuple())
            histories = [h for h in histories if h.creation_date >= ts]
        return histories

    def last_history(self):
        """Get last (most recent) scan history if exists.

        :return: An instance of :class:`tenable_io.api.models.ScanDetailsHistory` if exists, otherwise None.
        """
        histories = self.histories()
        return max(histories, key=lambda history: history.history_id) if len(histories) else None

    def launch(self, wait=True, alt_targets=None):
        """Launch the scan.

        :param wait: If True, the method blocks until the scan's status is not \
        :class:`tenable_io.api.models.Scan`.STATUS_PENDING. Default is False.

        :param alt_targets: String of comma separated alternative targets or list of alternative target strings.
        :return: The same ScanRef instance.
        """
        if isinstance(alt_targets, six.string_types):
            alt_targets = [alt_targets]

        self._client.scans_api.launch(
            self.id,
            ScanLaunchRequest(alt_targets=alt_targets)
        )
        if wait:
            util.wait_until(lambda context: self.status(_context=context) not in ScanHelper.STATUSES_PENDING,
                            context={})
        return self

    def name(self, history_id=None):
        """Get the name of the scan.

        :param history_id: The scan history to get name for, None for most recent. Default to None.
        :return: The name.
        """
        return self.details(history_id=history_id).info.name

    def folder(self, history_id=None):
        """Get the folder the scan is in.

        :param history_id: The scan history to get folder for, None for most recent. Default to None.
        :return: An instance of FolderRef.
        """
        from tenable_io.helpers.folder import FolderRef
        return FolderRef(self._client, self.details(history_id=history_id).info.folder_id)

    def move_to(self, folder):
        """Move the scan to a folder.

        :param folder: An instance of FolderRef identifying the folder to move the scan to.
        :return: The same ScanRef instance.
        """
        from tenable_io.helpers.folder import FolderRef
        assert isinstance(folder, FolderRef)
        self._client.scans_api.folder(self.id, folder.id)
        return self

    def trash(self):
        """Move the scan into the trash folder.

        :return: The same ScanRef instance.
        """
        trash_folder = self._client.folder_helper.trash_folder()
        self.move_to(trash_folder)
        return self

    def pause(self, wait=True):
        """Pause the scan.

        :param wait: If True, the method blocks until the scan's status is not \
        :class:`tenable_io.api.models.Scan`.STATUS_PAUSING. Default is False.
        :return: The same ScanRef instance.
        """
        self._client.scans_api.pause(self.id)
        if wait:
            util.wait_until(lambda context: self.status(_context=context) != Scan.STATUS_PAUSING, context={})
        return self

    def resume(self, wait=True):
        """Resume the scan.

        :param wait: If True, the method blocks until the scan's status is not \
        :class:`tenable_io.api.models.Scan`.STATUS_RESUMING. Default is False.
        :return: The same ScanRef instance.
        """
        self._client.scans_api.resume(self.id)
        if wait:
            util.wait_until(lambda context: self.status(_context=context) != Scan.STATUS_RESUMING, context={})
        return self

    def status(self, history_id=None, _context=None):
        """Get the scan's status.

        :param history_id: The scan history to get status for, None for most recent. Default to None.
        :return: The same ScanRef instance.
        """
        # _context allows caller to keep the context for subsequent calls, this is a temporary workaround to the cheaper
        # status API requires a history_id, which is not always available during the pending phases when a scan is
        # starting.
        if _context is not None and history_id is None:
            history_id = _context.get('history_id')

        if history_id is not None:
            status = self._client.scans_api.history(self.id, history_id=history_id).status
        else:
            details = self.details(history_id=history_id)
            if _context and len(details.history) > 0:
                _context['history_id'] = details.history[0].history_id
            status = details.info.status
        return status

    def stop(self, wait=True):
        """Stop the scan.

        :param wait: If True, the method blocks until the scan's status is stopped. Default is False.
        :return: The same ScanRef instance.
        """
        self._client.scans_api.stop(self.id)
        if wait:
            self.wait_until_stopped()
        return self

    def stopped(self, history_id=None, _context=None):
        """Check if the scan is stopped.

        :param history_id: The scan history to check, None for most recent. Default to None.
        :return: True if stopped, False otherwise.
        """
        return self.status(history_id=history_id, _context=_context) in ScanHelper.STATUSES_STOPPED

    def wait_or_cancel_after(self, seconds):
        """Blocks until the scan is stopped, or cancel if it isn't stopped within the specified seconds.

        :param seconds: The maximum amount of seconds the method should block before canceling the scan.
        :return: The same ScanRef instance.
        """
        start_time = time.time()
        util.wait_until(lambda: time.time() - start_time > seconds or self.stopped())
        if not self.stopped():
            self.stop()
        return self

    def wait_until_stopped(self, history_id=None):
        """Blocks until the scan is stopped.

        :param history_id: The scan history to wait for, None for most recent. Default to None.
        :return: The same ScanRef instance.
        """
        util.wait_until(lambda context: self.stopped(history_id=history_id, _context=context), context={})
        return self
