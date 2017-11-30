import pytest

from tenable_io.exceptions import TenableIOApiException
from tenable_io.api.models import Scan, ScanSettings, Scanner, ScannerList, ScannerScanList
from tenable_io.api.scanners import ScannerControlRequest, ScannerEditRequest
from tenable_io.api.scans import ScanCreateRequest, ScanLaunchRequest

from tests.base import BaseTest
from tests.config import TenableIOTestConfig


class TestScannersApi(BaseTest):

    @pytest.fixture(scope='class')
    def scanner(self, client):
        """
        Get scanner for testing.
        """
        scanner_list = client.scanners_api.list()
        assert len(scanner_list.scanners) > 0, u'At least one scanner.'

        test_scanner = scanner_list.scanners[0]

        for scanner in scanner_list.scanners:
            if scanner.name == 'US Cloud Scanner':
                test_scanner = scanner

        yield test_scanner

    @pytest.fixture(scope='class')
    def template(self, client):
        """
        Get scan template for testing.
        """
        template_list = client.editor_api.list('scan')
        assert len(template_list.templates) > 0, u'At least one scan template.'

        test_templates = [t for t in template_list.templates if t.name == TenableIOTestConfig.get('scan_template_name')]
        assert len(test_templates) > 0, u'At least one test template.'

        yield test_templates[0]

    @pytest.fixture(scope='class')
    def scan(self, app, client, scanner, template):
        """
        Create scan for testing. Ensure there is one active (running or paused) scan in given scanner.
        """
        scan_id = client.scans_api.create(
            ScanCreateRequest(
                template.uuid,
                ScanSettings(
                    app.session_name('test_scanners'),
                    TenableIOTestConfig.get('scan_text_targets'),
                    scanner_id=scanner.id
                )
            )
        )

        client.scans_api.launch(scan_id, ScanLaunchRequest())
        scan_details = client.scans_api.details(scan_id)
        assert scan_details.info.status in [Scan.STATUS_PENDING, Scan.STATUS_INITIALIZING, Scan.STATUS_RUNNING], \
            u'Scan is in launched state.'

        scan_details = self.wait_until(lambda: client.scans_api.details(scan_id),
                                       lambda details: details.info.status in [
                                           Scan.STATUS_COMPLETED, Scan.STATUS_RUNNING])
        assert scan_details.info.status == Scan.STATUS_RUNNING, u'Scan should be running to test pause.'

        client.scans_api.pause(scan_id)
        scan_details = client.scans_api.details(scan_id)
        assert scan_details.info.status in [Scan.STATUS_PAUSED, Scan.STATUS_PAUSING], u'Scan is pausing.'
        scan_details = self.wait_until(lambda: client.scans_api.details(scan_id),
                                       lambda details: details.info.status in [Scan.STATUS_PAUSED])
        assert scan_details.info.status == Scan.STATUS_PAUSED, u'Scan is paused.'

        yield scan_details

        try:
            client.scans_api.delete(scan_id)
        except TenableIOApiException:
            # This happens when the scan is not idling.
            client.scans_api.stop(scan_id)
            self.wait_until(lambda: client.scans_api.details(scan_id),
                            lambda details: details.info.status in [
                                Scan.STATUS_CANCELED, Scan.STATUS_COMPLETED, Scan.STATUS_EMPTY])
            client.scans_api.delete(scan_id)

    def test_get_scans_control_scans(self, client, scanner, scan):
        scan_id = scan.info.object_id

        scan_list = client.scanners_api.get_scans(scanner.id)
        assert isinstance(scan_list, ScannerScanList), u'Get request returns type.'
        assert len(scan_list.scans) > 0, u'At least one test scan.'

        scan_uuid = scan.info.uuid
        test_scans = [s for s in scan_list.scans if s.id == scan_uuid]
        assert len(test_scans) == 1, u'Must contain test scan.'

        client.scanners_api.control_scans(scanner.id, scan_uuid, ScannerControlRequest(u'resume'))
        scan_details = self.wait_until(lambda: client.scans_api.details(scan_id),
                                       lambda details: details.info.status in [
                                           Scan.STATUS_COMPLETED, Scan.STATUS_RUNNING])
        assert scan_details.info.status == Scan.STATUS_RUNNING, u'Scan must be resumed.'

        client.scanners_api.control_scans(scanner.id, scan_uuid, ScannerControlRequest(u'pause'))
        scan_details = self.wait_until(lambda: client.scans_api.details(scan_id),
                                       lambda details: details.info.status in [Scan.STATUS_PAUSED])
        assert scan_details.info.status == Scan.STATUS_PAUSED, u'Scan is paused.'

    def test_details(self, client, scanner):
        scanner_details = client.scanners_api.details(scanner.id)
        assert isinstance(scanner_details, Scanner), u'Get request returns type.'

    def test_edit(self, client, scanner):
        response = client.scanners_api.edit(scanner.id, ScannerEditRequest())
        assert response == True, u'Method should return True if 200 response is received.'

    @pytest.mark.xfail(reason="CI-16038")
    def test_get_scanner_key(self, client, scanner):
        key = client.scanners_api.get_scanner_key(scanner.id)
        assert key, u'Get request returns valid key.'

    def test_list(self, client):
        scanners = client.scanners_api.list()
        assert isinstance(scanners, ScannerList), u'Get request returns type.'
        assert len(scanners.scanners) > 0, u'Must contain at least one scanner.'

    def test_toggle_link_state(self, client, scanner):
        with pytest.raises(TenableIOApiException) as e:
            client.scanners_api.toggle_link_state(scanner.id, None)
        assert e.value.response.status_code != 404, u'Request cannot return with 404.'
