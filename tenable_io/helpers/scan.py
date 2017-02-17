import six
import os
import re
import time

from datetime import datetime

from tenable_io.api.models import Scan, ScanSettings, Template
from tenable_io.api.scans import ScansApi, ScanCreateRequest, ScanExportRequest, ScanImportRequest, ScanLaunchRequest
from tenable_io.exceptions import TenableIOException
from tenable_io.util import wait_until


class ScanHelper(object):

    STATUSES_STOPPED = [
        Scan.STATUS_ABORTED,
        Scan.STATUS_CANCELED,
        Scan.STATUS_COMPLETED,
        Scan.STATUS_IMPORTED,
        Scan.STATUS_EMPTY,
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
        scan_detail = self._client.scans_api.details(id)
        return ScanRef(self._client, scan_detail.info.object_id)

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

    def import_scan(self, path):
        """Uploads and then imports scan report.

        :param path: Path of the scan report.
        :return: ScanRef referenced by id if exists.
        """
        if not os.path.isfile(path):
            raise TenableIOException(u'File does not exist at path.')

        with open(path, 'rb') as upload_file:
            upload_file_name = self._client.file_api.upload(upload_file)

        imported_scan_id = self._client.scans_api.import_scan(ScanImportRequest(upload_file_name))

        return self.id(imported_scan_id)


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

    def delete(self):
        """Delete the scan.

        :return: The same ScanRef instance.
        """
        self._client.scans_api.delete(self.id)
        return self

    def details(self, history_id=None):
        """Get the scan detail.

        :return: An instance of :class:`tenable_io.api.models.ScanDetails`.
        """
        return self._client.scans_api.details(self.id, history_id=history_id)

    def download(self, path, history_id=None, format=ScanExportRequest.FORMAT_PDF, file_open_mode='wb'):
        """Download a scan report.

        :param path: The file path to save the report to.
        :param format: The report format. Default to :class:`tenable_io.api.models.ScanDetails`.FORMAT_PDF.
        :param file_open_mode: The open mode to the file output. Default to "wb".
        :param history_id: A specific scan history ID, None for the most recent scan history. default to None.
        :return: The same ScanRef instance.
        """
        self.wait_until_stopped(history_id=history_id)

        file_id = self._client.scans_api.export_request(
            self.id,
            ScanExportRequest(format=format),
            history_id
        )
        wait_until(
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
        :return: A list of :class:`tenable_io.api.models.ScanHistory`.
        """
        histories = self.details().history
        if since:
            assert isinstance(since, datetime), '`since` parameter should be an instance of datetime.'
            ts = time.mktime(since.timetuple())
            histories = [h for h in histories if h.creation_date >= ts]
        return histories

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
            wait_until(lambda: self.status() not in Scan.STATUS_PENDING)
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
            wait_until(lambda: self.status() != Scan.STATUS_PAUSING)
        return self

    def resume(self, wait=True):
        """Resume the scan.

        :param wait: If True, the method blocks until the scan's status is not \
        :class:`tenable_io.api.models.Scan`.STATUS_RESUMING. Default is False.
        :return: The same ScanRef instance.
        """
        self._client.scans_api.resume(self.id)
        if wait:
            wait_until(lambda: self.status() != Scan.STATUS_RESUMING)
        return self

    def status(self, history_id=None):
        """Get the scan's status.

        :param history_id: The scan history to get status for, None for most recent. Default to None.
        :return: The same ScanRef instance.
        """
        return self.details(history_id=history_id).info.status

    def stop(self, wait=True):
        """Stop the scan.

        :param wait: If True, the method blocks until the scan's status is stopped. Default is False.
        :return: The same ScanRef instance.
        """
        self._client.scans_api.stop(self.id)
        if wait:
            self.wait_until_stopped()
        return self

    def stopped(self, history_id=None):
        """Check if the scan is stopped.

        :param history_id: The scan history to check, None for most recent. Default to None.
        :return: True if stopped, False otherwise.
        """
        return self.status(history_id=history_id) in ScanHelper.STATUSES_STOPPED

    def wait_or_cancel_after(self, seconds):
        """Blocks until the scan is stopped, or cancel if it isn't stopped within the specified seconds.

        :param seconds: The maximum amount of seconds the method should block before canceling the scan.
        :return: The same ScanRef instance.
        """
        start_time = time.time()
        wait_until(lambda: time.time() - start_time > seconds or self.stopped())
        if not self.stopped():
            self.stop()
        return self

    def wait_until_stopped(self, history_id=None):
        """Blocks until the scan is stopped.

        :param history_id: The scan history to wait for, None for most recent. Default to None.
        :return: The same ScanRef instance.
        """
        wait_until(lambda: self.stopped(history_id=history_id))
        return self
