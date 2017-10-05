import os
import pytest

from tenable_io.exceptions import TenableIOApiException
from tenable_io.api.models import Folder, Scan, ScanHostDetails, ScanList, ScanSettings
from tenable_io.api.scans import ScansApi, ScanConfigureRequest, ScanCreateRequest, \
    ScanExportRequest, ScanImportRequest, ScanLaunchRequest

from tests.base import BaseTest
from tests.config import TenableIOTestConfig


class TestScansApi(BaseTest):

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
    def scan_id(self, app, client, template):
        """
        Create a scan for testing.
        """
        scan_id = client.scans_api.create(
            ScanCreateRequest(
                template.uuid,
                ScanSettings(
                    app.session_name('test_scans'),
                    TenableIOTestConfig.get('scan_text_targets'),
                )
            )
        )
        yield scan_id

        try:
            client.scans_api.delete(scan_id)
        except TenableIOApiException:
            # This happens when the scan is not idling.
            client.scans_api.stop(scan_id)
            self.wait_until(lambda: client.scans_api.details(scan_id),
                            lambda details: details.info.status in [
                                Scan.STATUS_CANCELED, Scan.STATUS_COMPLETED, Scan.STATUS_EMPTY])
            client.scans_api.delete(scan_id)

    @pytest.fixture(scope='class')
    def folder_id(self, app, client):
        folder_id = client.folders_api.create(app.session_name('test_scans', length=5))
        yield folder_id
        client.folders_api.delete(folder_id)

    @pytest.fixture(scope='class')
    def main_folder_id(self, client):
        folder_list = client.folders_api.list()
        main_folder_id = None
        for f in folder_list.folders:
            if f.type == Folder.TYPE_MAIN:
                main_folder_id = f.id
        assert main_folder_id is not None, u'Main folder exists.'
        yield main_folder_id

    def test_list_return_correct_type(self, client):
        scan = client.scans_api.list()
        assert isinstance(scan, ScanList), u'The `list` method returns type.'

    def test_create_launch_pause_resume_history_stop_delete_host_details(self, client, scan_id):
        scan_details = client.scans_api.details(scan_id)
        assert scan_details.info.status in [Scan.STATUS_CANCELED, Scan.STATUS_COMPLETED, Scan.STATUS_EMPTY], \
            u'Scan is in idling state.'

        # Launch the scan.
        client.scans_api.launch(
            scan_id,
            ScanLaunchRequest()
        )
        scan_details = client.scans_api.details(scan_id)
        assert scan_details.info.status in [Scan.STATUS_PENDING, Scan.STATUS_RUNNING], u'Scan is in launched state.'

        scan_details = self.wait_until(lambda: client.scans_api.details(scan_id),
                                       lambda details: details.info.status in [
                                           Scan.STATUS_COMPLETED, Scan.STATUS_RUNNING])
        assert scan_details.info.status == Scan.STATUS_RUNNING, u'Scan should be running to test pause.'

        # Pause the running scan.
        client.scans_api.pause(scan_id)
        scan_details = client.scans_api.details(scan_id)
        assert scan_details.info.status in [Scan.STATUS_PAUSED, Scan.STATUS_PAUSING], u'Scan is pausing.'
        scan_details = self.wait_until(lambda: client.scans_api.details(scan_id),
                                       lambda details: details.info.status in [Scan.STATUS_PAUSED])
        assert scan_details.info.status == Scan.STATUS_PAUSED, u'Scan is paused.'

        # Resume the paused scan.
        client.scans_api.resume(scan_id)
        scan_details = client.scans_api.details(scan_id)
        assert scan_details.info.status in [Scan.STATUS_RESUMING, Scan.STATUS_RUNNING], u'Scan is resuming.'

        scan_details = self.wait_until(lambda: client.scans_api.details(scan_id),
                                       lambda details: details.info.status in [
                                           Scan.STATUS_COMPLETED, Scan.STATUS_RUNNING])
        assert scan_details.info.status == Scan.STATUS_RUNNING, u'Scan is running.'

        # Stop the running scan.
        client.scans_api.stop(scan_id)
        scan_details = client.scans_api.details(scan_id)
        assert scan_details.info.status in [Scan.STATUS_CANCELED, Scan.STATUS_STOPPING], u'Scan is resuming.'

        scan_details = self.wait_until(lambda: client.scans_api.details(scan_id),
                                       lambda details: details.info.status in [Scan.STATUS_CANCELED])
        assert scan_details.info.status == Scan.STATUS_CANCELED, u'Scan is canceled.'

        # Test the history API.
        assert len(scan_details.history) > 0, u'Scan has at least one history.'
        history_id = scan_details.history[0].history_id
        history = client.scans_api.history(scan_id, history_id)
        assert history.status == scan_details.info.status, u'Scan history reports same status as scan details.'

        # Test the scan host details API.
        assert len(scan_details.hosts) > 0, u'Scan has at least one host.'
        host_details = client.scans_api.host_details(scan_id, scan_details.hosts[0].host_id)
        assert isinstance(host_details, ScanHostDetails), u'The `host_details` method returns correct type.'

    def test_export_import(self, app, client, scan_id):

        # Cannot export on a test that has never been launched, therefore launch the scan first.
        client.scans_api.launch(
            scan_id,
            ScanLaunchRequest()
        )
        self.wait_until(lambda: client.scans_api.details(scan_id),
                        lambda details: details.info.status in [Scan.STATUS_COMPLETED, Scan.STATUS_RUNNING])

        # Stop the running scan.
        client.scans_api.stop(scan_id)
        self.wait_until(lambda: client.scans_api.details(scan_id),
                        lambda details: details.info.status in [Scan.STATUS_CANCELED])

        file_id = client.scans_api.export_request(
            scan_id,
            ScanExportRequest(
                format=ScanExportRequest.FORMAT_NESSUS
            )
        )
        assert file_id, u'The `export_request` method returns a valid file ID.'

        export_status = self.wait_until(lambda: client.scans_api.export_status(scan_id, file_id),
                                        lambda status: status == ScansApi.STATUS_EXPORT_READY)
        assert export_status == ScansApi.STATUS_EXPORT_READY, u'Scan export is ready.'

        iter_content = client.scans_api.export_download(scan_id, file_id, False)

        download_path = app.session_file_output('test_scan_export_import')
        assert not os.path.isfile(download_path), u'Scan report does not yet exist.'

        with open(download_path, 'wb') as fd:
            for chunk in iter_content:
                fd.write(chunk)
        assert os.path.isfile(download_path), u'Scan report is downloaded.'
        assert os.path.getsize(download_path) > 0, u'Scan report is not empty.'

        with open(download_path, 'rb') as fu:
            upload_file_name = client.file_api.upload(fu)
        assert upload_file_name, u'File `upload` method returns valid file name.'

        imported_scan_id = client.scans_api.import_scan(ScanImportRequest(upload_file_name))
        assert isinstance(imported_scan_id, int), u'Import request returns scan id.'

        imported_scan_details = client.scans_api.details(imported_scan_id)
        scan_details = client.scans_api.details(scan_id)
        assert imported_scan_details.info.name == scan_details.info.name, \
            u'Imported scan retains name of exported scan.'

        os.remove(download_path)
        client.scans_api.delete(imported_scan_id)

    def test_copy_delete(self, client, scan_id):
        scan = client.scans_api.copy(scan_id)
        assert scan.id != scan_id, u'Copied scan should not have same ID as the original scan.'
        client.scans_api.delete(scan.id)
        with pytest.raises(TenableIOApiException):
            client.scans_api.details(scan.id)

    def test_configure(self, app, client, scan_id):
        scan_details = client.scans_api.details(scan_id)

        before_name = scan_details.info.name
        after_name = app.session_name('test_scans_config', length=3)

        client.scans_api.configure(scan_id, ScanConfigureRequest(
            settings=ScanSettings(
                name=after_name,
                text_targets=TenableIOTestConfig.get('scan_template_name')
            )
        ))

        scan_details = client.scans_api.details(scan_id)
        assert scan_details.info.name == after_name, u'Name is reconfigured.'

        client.scans_api.configure(scan_id, ScanConfigureRequest(
            settings=ScanSettings(
                name=before_name,
                text_targets=TenableIOTestConfig.get('scan_template_name')
            )
        ))

        scan_details = client.scans_api.details(scan_id)
        assert scan_details.info.name == before_name, u'Name is reverted.'

    def test_folder(self, client, scan_id, folder_id, main_folder_id):
        scan_details = client.scans_api.details(scan_id)

        # When scan is just created, it can have None as folder_id which the API considers it in the main folder.
        before_folder_id = scan_details.info.folder_id or main_folder_id
        after_folder_id = folder_id

        client.scans_api.folder(scan_id, after_folder_id)
        scan_details = client.scans_api.details(scan_id)
        assert scan_details.info.folder_id == after_folder_id, u'Scan is moved to the new folder.'

        client.scans_api.folder(scan_id, before_folder_id)
        scan_details = client.scans_api.details(scan_id)
        assert scan_details.info.folder_id == before_folder_id, u'Scan is returned to the previous folder.'
