import os
import pytest

from tenable_io.api.models import Scan, ScanHostDetails, ScanList, ScanSettings, ScanDetails
from tenable_io.api.scans import ScansApi, ScanConfigureRequest, ScanExportRequest, ScanImportRequest, ScanLaunchRequest

from tests.config import TenableIOTestConfig
from tests.integration.api.utils.utils import wait_until


@pytest.mark.vcr()
def test_scans_create(new_scan):
    assert isinstance(new_scan, int), u'The `create` method did not return type `int`.'


@pytest.mark.vcr()
def test_scans_list(client):
    scan_list = client.scans_api.list()
    assert isinstance(scan_list, ScanList), u'The `list` method did not return type `ScannerList`.'


@pytest.mark.vcr()
def test_scans_details(client, new_scan):
    scan_details = client.scans_api.details(new_scan)
    assert isinstance(scan_details, ScanDetails), u'The `details` method did not return type `ScanDetails`.'


@pytest.mark.vcr()
def test_scans_delete(client, new_scan):
    assert client.scans_api.delete(new_scan), u'The scan was not deleted.'


@pytest.mark.vcr()
def test_scans_copy(client, new_scan):
    scan_id = new_scan
    copy_of_scan = client.scans_api.copy(scan_id)
    assert isinstance(copy_of_scan, Scan), u'The `copy` method did not return type `Scan`.'
    scan_details = client.scans_api.details(scan_id)
    assert scan_details.info.name == copy_of_scan.name.strip('Copy of '), \
        u'Expected the copy of the scan to have the same name as the original.'


@pytest.mark.vcr()
def test_scans_configure(client, new_scan):
    scan_id = new_scan
    after_name = 'scan_name_edit'
    client.scans_api.configure(scan_id, ScanConfigureRequest(
        settings=ScanSettings(
            name=after_name,
            text_targets=TenableIOTestConfig.get('scan_template_name')
        )
    ))

    scan_details = client.scans_api.details(scan_id)
    assert scan_details.info.name == after_name, u'The returned scan name should match the the edited value.'


@pytest.mark.vcr()
def test_scans_folder(client, new_folder, new_scan):
    assert client.scans_api.folder(new_scan, new_folder), u'The scan was not moved.'


@pytest.mark.vcr()
def test_scans_latest_status(client, new_scan):
    latest_status = client.scans_api.latest_status(new_scan)
    assert latest_status == 'empty', u'Expected a status of `empty` on a scan that has never been run.'


@pytest.mark.extended_testing
@pytest.mark.vcr()
def test_scans_control_endpoints(client, new_scan):
    scan_id = new_scan
    scan_details = client.scans_api.details(scan_id)
    assert scan_details.info.status in [Scan.STATUS_CANCELED, Scan.STATUS_COMPLETED, Scan.STATUS_EMPTY], \
        u'Scan is not in an idling state.'

    # Launch the scan.
    client.scans_api.launch(
        scan_id,
        ScanLaunchRequest()
    )
    scan_details = client.scans_api.details(scan_id)
    assert scan_details.info.status in [Scan.STATUS_PENDING, Scan.STATUS_INITIALIZING, Scan.STATUS_RUNNING], \
        u'The scan is not launching.'

    scan_details = wait_until(lambda: client.scans_api.details(scan_id),
                              lambda details: details.info.status in [
                                       Scan.STATUS_COMPLETED, Scan.STATUS_RUNNING])
    assert scan_details.info.status == Scan.STATUS_RUNNING, u'The scan is not running.'

    # Pause the running scan.
    client.scans_api.pause(scan_id)
    scan_details = client.scans_api.details(scan_id)
    assert scan_details.info.status in [Scan.STATUS_PAUSED, Scan.STATUS_PAUSING], u'The scan is not pausing.'
    scan_details = wait_until(lambda: client.scans_api.details(scan_id),
                              lambda details: details.info.status in [Scan.STATUS_PAUSED])
    assert scan_details.info.status == Scan.STATUS_PAUSED, u'The scan is not paused.'

    # Resume the paused scan.
    client.scans_api.resume(scan_id)
    scan_details = client.scans_api.details(scan_id)
    assert scan_details.info.status in [Scan.STATUS_RESUMING, Scan.STATUS_RUNNING], u'The scan is not resuming.'

    scan_details = wait_until(lambda: client.scans_api.details(scan_id),
                              lambda details: details.info.status in [
                                       Scan.STATUS_COMPLETED, Scan.STATUS_RUNNING])
    assert scan_details.info.status == Scan.STATUS_RUNNING, u'The scan is not running.'

    # Stop the running scan.
    client.scans_api.stop(scan_id)
    scan_details = client.scans_api.details(scan_id)
    assert scan_details.info.status in [Scan.STATUS_CANCELED, Scan.STATUS_STOPPING], u'The scan is not resuming.'

    scan_details = wait_until(lambda: client.scans_api.details(scan_id),
                              lambda details: details.info.status in [Scan.STATUS_CANCELED])
    assert scan_details.info.status == Scan.STATUS_CANCELED, u'The scan was not canceled.'

    # Test the history API.
    assert len(scan_details.history) > 0, u'The scan should have at least one history.'
    history_id = scan_details.history[0].history_id
    history = client.scans_api.history(scan_id, history_id)
    assert history.status == scan_details.info.status, u'Scan history should report same status as scan details.'

    # Test the scan host details API.
    assert len(scan_details.hosts) > 0, u'Expected the scan to have at least one host.'
    host_details = client.scans_api.host_details(scan_id, scan_details.hosts[0].host_id)
    assert isinstance(host_details, ScanHostDetails), \
        u'The `host_details` method did not return type `ScanHostDetails`.'


@pytest.mark.extended_testing
@pytest.mark.skip
@pytest.mark.vcr()
def test_scans_export_import(client, new_scan):
    scan_id = new_scan
    # Cannot export on a test that has never been launched, therefore launch the scan first.
    client.scans_api.launch(
        scan_id,
        ScanLaunchRequest()
    )
    wait_until(lambda: client.scans_api.details(scan_id),
               lambda details: details.info.status in [Scan.STATUS_COMPLETED])

    file_id = client.scans_api.export_request(
        scan_id,
        ScanExportRequest(
            format=ScanExportRequest.FORMAT_NESSUS
        )
    )
    assert file_id, u'The `export_request` method did not return a valid file ID.'

    export_status = wait_until(lambda: client.scans_api.export_status(scan_id, file_id),
                               lambda status: status == ScansApi.STATUS_EXPORT_READY)
    assert export_status == ScansApi.STATUS_EXPORT_READY, u'Scan export is not ready.'

    iter_content = client.scans_api.export_download(scan_id, file_id, False)

    download_path = 'test_scan_export_import'
    assert not os.path.isfile(download_path), u'Scan report does not yet exist.'

    with open(download_path, 'wb') as fd:
        for chunk in iter_content:
            fd.write(chunk)
    assert os.path.isfile(download_path), u'Scan report has not downloaded.'
    assert os.path.getsize(download_path) > 0, u'Scan report is not empty.'

    with open(download_path, 'rb') as fu:
        upload_file_name = client.file_api.upload(fu)
    assert upload_file_name, u'File `upload` method did not return a valid file name.'

    imported_scan_id = client.scans_api.import_scan(ScanImportRequest(upload_file_name))
    assert isinstance(imported_scan_id, int),  u'The `import_scan` method did not return type `int`.'

    imported_scan_details = client.scans_api.details(imported_scan_id)
    scan_details = client.scans_api.details(scan_id)
    assert imported_scan_details.info.name == scan_details.info.name, \
        u'Imported scan retains name of exported scan.'

    os.remove(download_path)
