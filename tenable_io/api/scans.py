from json import loads

from tenable_io.api.base import BaseApi
from tenable_io.api.models import Scan, ScanCredentials, ScanDetails, ScanHistory, \
    ScanHostDetails, ScanList, ScanSettings
from tenable_io.api.base import BaseRequest


class ScansApi(BaseApi):

    STATUS_EXPORT_READY = u'ready'

    def configure(self, scan_id=None, scan_configure=None, schedule_uuid=None):
        """Configure an existing scan.

        :param scan_id: The scan ID.
        :param scan_configure: An instance of :class:`ScanConfigureRequest`.
        :param schedule_uuid: The scan schedule UUID, this value will be used when specified and when scan_id is not present.
        :raise TenableIOApiException:  When API error is encountered.
        :return: The ID of scan just configured.
        """
        response = self._client.put('scans/%(scan_id)s',
                                    scan_configure,
                                    path_params={'scan_id': scan_id or schedule_uuid})
        return loads(response.text).get('scan', {}).get('id')

    def create(self, scan_create, return_uuid=False):
        """Create a scan.

        :param scan_create: An instance of :class:`ScanCreateRequest`.
        :param return_uuid: Optional param to return uuid rather than numeric id as the method response.
        :raise TenableIOApiException:  When API error is encountered.
        :return: The ID of scan just created.
        """
        response = self._client.post('scans', scan_create)
        return loads(response.text).get('scan', {}).get('id') \
            if not return_uuid \
            else loads(response.text).get('scan', {}).get('uuid')

    def copy(self, scan_id=None, schedule_uuid=None):
        """Creates a copy of a scan.

        :param scan_id: The scan ID.
        :param schedule_uuid: The scan schedule UUID, this value will be used when specified and when scan_id is not present.
        :return: An instance of :class:`tenable_io.api.models.Scan`.
        """
        response = self._client.post('scans/%(scan_id)s/copy',
                                     {},
                                     path_params={'scan_id': scan_id or schedule_uuid})
        return Scan.from_json(response.text)

    def delete(self, scan_id=None, schedule_uuid=None):
        """Delete a scan. NOTE: Scans in running, paused or stopping states can not be deleted.

        :raise TenableIOApiException:  When API error is encountered.
        :param scan_id: The scan ID.
        :param schedule_uuid: The scan schedule UUID, this value will be used when specified and when scan_id is not present.
        :return: True if successful.
        """
        self._client.delete('scans/%(scan_id)s', path_params={'scan_id': scan_id or schedule_uuid})
        return True

    def details(self, scan_id=None, history_id=None, schedule_uuid=None):
        """Return details of the given scan.

        :param scan_id: The scan ID.
        :param history_id: The historical data ID.
        :param schedule_uuid: The scan schedule UUID, this value will be used when specified and when scan_id is not present.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.ScanDetails`.
        """
        response = self._client.get('scans/%(scan_id)s',
                                    path_params={'scan_id': scan_id or schedule_uuid},
                                    params={'history_id': history_id} if history_id else None)

        return ScanDetails.from_json(response.text)

    def export_download(self, scan_id=None, file_id=None, stream=True, chunk_size=1024, is_was=False, schedule_uuid=None):
        """Download an exported scan.

        :param scan_id: The scan ID.
        :param file_id: The file ID.
        :param stream: Default to True. If False, the response content will be immediately downloaded.
        :param chunk_size: If Stream=False, data is returned as a single chunk.\
         If Stream=True, it's the number of bytes it should read into memory.
        :param is_was: A flag that specifies that the scan is a WAS type scan.
        :param schedule_uuid: The scan schedule UUID, this value will be used when specified and when scan_id is not present.
        :raise TenableIOApiException:  When API error is encountered.
        :return: The downloaded file.
        """
        response = self._client.get('scans/%(scan_id)s/export/%(file_id)s/download',
                                    path_params={'scan_id': scan_id or schedule_uuid, 'file_id': file_id},
                                    params={'type': ScanExportRequest.WAS_EXPORT_TYPE} if is_was else None,
                                    stream=stream)
        return response.iter_content(chunk_size=chunk_size)

    def export_request(self, scan_id=None, scan_export=None, history_id=None, is_was=False, schedule_uuid=None):
        """Export the given scan. Once requested, the file can be downloaded using the export\
         download method upon receiving a "ready" status from the export status method.

        :param scan_id: The scan ID.
        :param scan_export: An instance of :class:`ScanExportRequest`.
        :param history_id: The history ID of historical data.
        :param is_was: A flag that specifies that the scan is a WAS type scan.
        :param schedule_uuid: The scan schedule UUID, this value will be used when specified and when scan_id is not present.
        :raise TenableIOApiException:  When API error is encountered.
        :return: The file ID.
        """
        assert isinstance(scan_export, ScanExportRequest)
        params = {'history_id': history_id if history_id else None,
                  'type': ScanExportRequest.WAS_EXPORT_TYPE if is_was else None}
        response = self._client.post('scans/%(scan_id)s/export',
                                     scan_export,
                                     path_params={'scan_id': scan_id or schedule_uuid},
                                     params={k: v for k, v in params.items() if v is not None})
        return loads(response.text).get('file')

    def export_status(self, scan_id=None, file_id=None, is_was=False, schedule_uuid=None):
        """Check the file status of an exported scan. When an export has been requested,\
         it is necessary to poll this endpoint until a "ready" status is returned,\
          at which point the file is complete and can be downloaded using the export download endpoint.

        :param scan_id: The scan ID.
        :param file_id: The file ID.
        :param is_was: A flag that specifies that the scan is a WAS type scan.
        :param schedule_uuid: The scan schedule UUID, this value will be used when specified and when scan_id is not present.
        :raise TenableIOApiException:  When API error is encountered.
        :return: The file status.
        """
        response = self._client.get('scans/%(scan_id)s/export/%(file_id)s/status',
                                    path_params={'scan_id': scan_id or schedule_uuid, 'file_id': file_id},
                                    params={'type': ScanExportRequest.WAS_EXPORT_TYPE} if is_was else None)
        return loads(response.text).get('status')

    def folder(self, scan_id=None, folder_id=None, schedule_uuid=None):
        """Move to a scan to a folder.

        :param scan_id: The scan ID.
        :param folder_id: The folder ID.
        :param schedule_uuid: The scan schedule UUID, this value will be used when specified and when scan_id is not present.
        :raise TenableIOApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.put('scans/%(scan_id)s/folder',
                         {'folder_id': folder_id},
                         path_params={'scan_id': scan_id or schedule_uuid})
        return True

    def history(self, scan_id=None, history_id=None, schedule_uuid=None):
        """Returns a scan history.

        :param scan_id: The scan ID.
        :param history_id: The historical data ID.
        :param schedule_uuid: The scan schedule UUID, this value will be used when specified and when scan_id is not present.
        :return: An instance of :class:`tenable_io.api.models.ScanHistory`.
        """
        response = self._client.get('scans/%(scan_id)s/history/%(history_id)s',
                                    path_params={'scan_id': scan_id or schedule_uuid, 'history_id': history_id})
        return ScanHistory.from_json(response.text)

    def host_details(self, scan_id=None, host_id=None, schedule_uuid=None):
        """Returns details for the given host.

        :param scan_id: The scan ID.
        :param host_id: The host ID.
        :param schedule_uuid: The scan schedule UUID, this value will be used when specified and when scan_id is not present.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.ScanHostDetails`.
        """
        response = self._client.get('scans/%(scan_id)s/hosts/%(host_id)s',
                                    path_params={'scan_id': scan_id or schedule_uuid, 'host_id': host_id})
        return ScanHostDetails.from_json(response.text)

    def import_scan(self, scan_import, include_aggregate=True):
        """Import an existing scan which has been uploaded using :func:`TenableIO.FileApi.upload`

        :param scan_import: An instance of :class:`ScanImportRequest`.
        :param include_aggregate: Boolean indicating whether scan data should appear in Workbenches.
        :raise TenableIOApiException:  When API error is encountered.
        :return: The ID of the imported scan.
        """
        aggregate_option = 0
        if include_aggregate:
            aggregate_option = 1

        response = self._client.post('scans/import?include_aggregate=%(include_aggregate)s',
                                     scan_import,
                                     path_params={'include_aggregate': aggregate_option})
        return loads(response.text).get('scan', {}).get('id')

    def launch(self, scan_id=None, scan_launch_request=None, schedule_uuid=None):
        """Launch a scan.

        :param scan_id: The scan ID.
        :param scan_launch_request: An instance of :class:`ScanLaunchRequest`.
        :param schedule_uuid: The scan schedule UUID, this value will be used when specified and when scan_id is not present.
        :raise TenableIOApiException:  When API error is encountered.
        :return: The scan uuid.
        """
        assert isinstance(scan_launch_request, ScanLaunchRequest)
        response = self._client.post('scans/%(scan_id)s/launch',
                                     scan_launch_request,
                                     path_params={'scan_id': scan_id or schedule_uuid})
        return loads(response.text).get('scan_uuid')

    def list(self, folder_id=None, last_modification_date=None):
        """Return the scan list.

        :param folder_id: The folder ID (optional).
        :param last_modification_date: Limit the results to those that have only changed since this time (optional).
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.ScanList`.
        """
        params = {'folder_id': folder_id, 'last_modification_date': last_modification_date}
        response = self._client.get('scans', params={k: v for (k, v) in params.items() if v})
        return ScanList.from_json(response.text)

    def pause(self, scan_id=None, schedule_uuid=None):
        """Pause a scan.

        :param scan_id: The scan ID.
        :param schedule_uuid: The scan schedule UUID, this value will be used when specified and when scan_id is not present.
        :raise TenableIOApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.post('scans/%(scan_id)s/pause', {}, path_params={'scan_id': scan_id or schedule_uuid})
        return True

    def resume(self, scan_id=None, schedule_uuid=None):
        """Resume a scan.

        :param scan_id: The scan ID.
        :param schedule_uuid: The scan schedule UUID, this value will be used when specified and when scan_id is not present.
        :raise TenableIOApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.post('scans/%(scan_id)s/resume', {}, path_params={'scan_id': scan_id or schedule_uuid})
        return True

    def stop(self, scan_id=None, schedule_uuid=None):
        """Stop a scan.

        :param scan_id: The scan ID.
        :param schedule_uuid: The scan schedule UUID, this value will be used when specified and when scan_id is not present.
        :raise TenableIOApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.post('scans/%(scan_id)s/stop', {}, path_params={'scan_id': scan_id or schedule_uuid})
        return True

    def latest_status(self, scan_id=None, schedule_uuid=None):
        """ Gets scan latest status.

        :param scan_id: The scan ID.
        :param schedule_uuid: The scan schedule UUID, this value will be used when specified and when scan_id is not present.
        :raise TenableIOApiException:  When API error is encountered.
        :return: the scan status.
        """
        response = self._client.get('scans/%(scan_id)s/latest-status',
                                    path_params={'scan_id': scan_id or schedule_uuid})
        return loads(response.text).get('status', '')


class ScanSaveRequest(BaseRequest):

    def __init__(
            self,
            uuid,
            settings,
            credentials
    ):
        assert isinstance(settings, ScanSettings)
        self.uuid = uuid
        self.settings = settings
        self.credentials = credentials

    def as_payload(self, filter_=None):
        payload = super(ScanSaveRequest, self).as_payload(True)
        if isinstance(self.settings, ScanSettings):
            payload.__setitem__('settings', self.settings.as_payload())
        else:
            payload.pop('settings', None)
        if self.credentials is not None and isinstance(self.credentials, ScanCredentials):
            payload.__setitem__('credentials', self.credentials.as_payload())
        else:
            payload.pop('credentials', None)
        return payload


class ScanCreateRequest(ScanSaveRequest):

    def __init__(
            self,
            uuid,
            settings=None,
            credentials=None,
    ):
        super(ScanCreateRequest, self).__init__(uuid, settings, credentials)


class ScanConfigureRequest(ScanSaveRequest):

    def __init__(
            self,
            uuid=None,
            settings=None,
            credentials=None,
    ):
        super(ScanConfigureRequest, self).__init__(uuid, settings, credentials)


class ScanExportRequest(BaseRequest):

    CHAPTER_COMPLIANCE = u'compliance'
    CHAPTER_COMPLIANCE_EXEC = u'compliance_exec'
    CHAPTER_CUSTOM_VULN_BY_HOST = u'vuln_by_host'
    CHAPTER_CUSTOM_VULN_BY_PLUGIN = u'vuln_by_plugin'
    CHAPTER_EXECUTIVE_SUMMARY = u'vuln_hosts_summary'
    CHAPTER_REMEDIATIONS = u'remediations'

    FORMAT_CSV = u'csv'
    FORMAT_DB = u'db'
    FORMAT_HTML = u'html'
    FORMAT_NESSUS = u'nessus'
    FORMAT_PDF = u'pdf'

    WAS_EXPORT_TYPE = u'web-app'

    def __init__(
            self,
            format,
            password=None,
            chapters=None,
    ):
        assert format in [
            ScanExportRequest.FORMAT_CSV,
            ScanExportRequest.FORMAT_DB,
            ScanExportRequest.FORMAT_HTML,
            ScanExportRequest.FORMAT_NESSUS,
            ScanExportRequest.FORMAT_PDF,
        ]
        assert chapters in [
            None,
            ScanExportRequest.CHAPTER_COMPLIANCE,
            ScanExportRequest.CHAPTER_COMPLIANCE_EXEC,
            ScanExportRequest.CHAPTER_CUSTOM_VULN_BY_HOST,
            ScanExportRequest.CHAPTER_CUSTOM_VULN_BY_PLUGIN,
            ScanExportRequest.CHAPTER_EXECUTIVE_SUMMARY,
            ScanExportRequest.CHAPTER_REMEDIATIONS,
        ]
        self.format = format
        self.password = password
        self.chapters = chapters

    def as_payload(self, filter_=None):
        return super(ScanExportRequest, self).as_payload(True)


class ScanImportRequest(BaseRequest):

    def __init__(
            self,
            file,
            folder_id=None,
            password=None
    ):
        self.file = file
        self.folder_id = folder_id
        self.password = password


class ScanLaunchRequest(BaseRequest):

    def __init__(
            self,
            alt_targets=None
    ):
        self.alt_targets = alt_targets
