from json import loads

from tenable_io.api.base import BaseApi, BaseRequest
from tenable_io.api.models import Scanner, ScannerAwsTargetList, ScannerList, ScannerScanList


class ScannersApi(BaseApi):

    def control_scans(self, scanner_id, scan_uuid, control_scan):
        """Pause, stop, or resume scan that is active on the scanner.

        :param scanner_id: The scanner ID.
        :param scan_uuid: The scan UUID.
        :param control_scan: An instance of :class:`ScannerControlRequest`.
        :raise TenableIOApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.post('scanners/%(scanner_id)s/scans/%(scan_uuid)s/control',
                          control_scan,
                          path_params={'scanner_id': scanner_id, 'scan_uuid': scan_uuid})
        return True

    def delete(self, scanner_id):
        """Deletes a scanner.

        :param scanner_id: The scanner ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.delete('scanners/%(scanner_id)s', path_params={'scanner_id': scanner_id})
        return True

    def details(self, scanner_id):
        """Returns details of a given scanner.

        :param scanner_id: The scanner ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.Scanner`.
        """
        response = self._client.get('scanners/%(scanner_id)s', path_params={'scanner_id': scanner_id})
        return Scanner.from_json(response.text)

    def edit(self, scanner_id, scanner_edit):
        """Edit the given scanner.

        :param scanner_id: The scanner ID.
        :param scanner_edit: An instance of :class:`ScannerEditRequest`.
        :raise TenableIOApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.put('scanners/%(scanner_id)s', scanner_edit, path_params={'scanner_id': scanner_id})
        return True

    def get_aws_targets(self, scanner_id):
        """Returns list of AWS scan targets of an AWS scanner.

        :param scanner_id: The scanner ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.ScannerAwsTargetList`.
        """
        response = self._client.get('scanners/%(scanner_id)s/aws-targets', path_params={'scanner_id': scanner_id})
        return ScannerAwsTargetList.from_json(response.text)

    def get_scanner_key(self, scanner_id):
        """Returns key of given scanner.

        :param scanner_id: The scanner ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: Scanner key.
        """
        response = self._client.get('scanners/%(scanner_id)s/key', path_params={'scanner_id': scanner_id})
        return loads(response.text).get('key')

    def get_scans(self, scanner_id):
        """Returns list of running scans on given scanner.

        :param scanner_id: The scanner ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.ScannerScanList`.
        """
        response = self._client.get('scanners/%(scanner_id)s/scans', path_params={'scanner_id': scanner_id})
        return ScannerScanList.from_json(response.text)

    def list(self):
        """Returns list of scanners.

        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.ScannerList`.
        """
        response = self._client.get('scanners')
        return ScannerList.from_json(response.text)

    def toggle_link_state(self, scanner_id, toggle_link):
        """Enables or disables link state of given scanner.

        :param scanner_id: The scanner ID.
        :param toggle_link: An instance of :class:`ScannerToggleRequest`.
        :raise TenableIOApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.put('scanners/%(scanner_id)s/link',
                         toggle_link,
                         path_params={'scanner_id': scanner_id})
        return True


class ScannerControlRequest(BaseRequest):

    ACTION_PAUSE = u'pause'
    ACTION_RESUME = u'resume'
    ACTION_STOP = u'stop'

    def __init__(
            self,
            action
    ):
        assert action in [
            ScannerControlRequest.ACTION_PAUSE,
            ScannerControlRequest.ACTION_RESUME,
            ScannerControlRequest.ACTION_STOP,
        ]
        self.action = action


class ScannerEditRequest(BaseRequest):

    def __init__(
            self,
            force_plugin_update=None,
            force_ui_update=None,
            finish_update=None,
            registration_code=None,
            aws_update_interval=None
    ):
        self.force_plugin_update = force_plugin_update
        self.force_ui_update = force_ui_update
        self.finish_update = finish_update
        self.registration_code = registration_code
        self.aws_update_interval = aws_update_interval


class ScannerToggleRequest(BaseRequest):

    LINK_DISABLE = 0
    LINK_ENABLE = 1

    def __init__(
            self,
            link
    ):
        assert link in [
            ScannerToggleRequest.LINK_DISABLE,
            ScannerToggleRequest.LINK_ENABLE
        ]
        self.link = link
