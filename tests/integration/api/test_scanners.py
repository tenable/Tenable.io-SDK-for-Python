import pytest

from tenable_io.api.models import Scan, Scanner, ScannerList, ScannerAwsTarget, ScannerAwsTargetList, ScannerScanList
from tenable_io.api.scans import ScanCreateRequest, ScanLaunchRequest, ScanSettings
from tenable_io.api.scanners import ScannerControlRequest, ScannerEditRequest, ScannerToggleRequest
from tests.config import TenableIOTestConfig

from tests.integration.api.utils.utils import wait_until


@pytest.mark.vcr()
def test_scanners_list(client):
    scanner_list = client.scanners_api.list()
    assert len(scanner_list.scanners) > 0, u'At least one scanner.'
    assert isinstance(scanner_list, ScannerList), u'The `list` method did not return type `ScannerList`.'
    for scanner in scanner_list.scanners:
        assert isinstance(scanner, Scanner), u'Should be a list of type `Scanner`.'


@pytest.mark.vcr()
def test_scanners_get_scanner_key(client, fetch_scanner):
    key = client.scanners_api.get_scanner_key(fetch_scanner.id)
    assert key, u'Scanner key was not returned'


@pytest.mark.skip('No AWS scanners are available')
@pytest.mark.vcr()
def test_scanners_get_aws_targets(client, fetch_scanner):
    targets = client.scanners_api.get_aws_targets(fetch_scanner.id)
    assert isinstance(targets, ScannerAwsTargetList), \
        u'The `get_aws_targets` method did not return type `ScannerAwsTargetList`.'
    for target in targets.aws_targets:
        assert isinstance(target, ScannerAwsTarget), u'Should be a list of type `ScannerAwsTarget`.'


@pytest.mark.vcr()
def test_scanners_details(client, fetch_scanner):
    scanner_details = client.scanners_api.details(fetch_scanner.id)
    assert isinstance(scanner_details, Scanner), u'The `details` method did not return type `Scanner`.'


@pytest.mark.vcr()
def test_scanner_edit(client, fetch_scanner):
    assert client.scanners_api.edit(fetch_scanner.id, ScannerEditRequest()), \
        u'The scanner was not edited.'


@pytest.mark.vcr()
def test_scanner_delete(client):
    scanner_list = client.scanners_api.list()
    assert len(scanner_list.scanners) > 0, u'At least one scanner.'

    test_scanner = scanner_list.scanners[0]

    for scanner in scanner_list.scanners:
        if 'sdk' in scanner.name:
            test_scanner = scanner

    assert client.scanners_api.delete(test_scanner.id), u'The scanner was not deleted.'


@pytest.mark.vcr()
def test_scanner_toggle(client, fetch_scanner):
    assert client.scanners_api.toggle_link_state(fetch_scanner.id, ScannerToggleRequest(ScannerToggleRequest.LINK_ENABLE)), \
        u'The scanner state was not toggled.'


@pytest.mark.vcr()
def test_scanner_control_scan(client, fetch_scanner):
    template_list = client.editor_api.list('scan')
    assert len(template_list.templates) > 0, u'Expected at least one scan template.'

    test_templates = [t for t in template_list.templates if t.name == 'basic']
    scan_id = client.scans_api.create(
        ScanCreateRequest(
            test_templates[0].uuid,
            ScanSettings(
                'test_scanners_scan',
                TenableIOTestConfig.get('scan_text_targets'),
                scanner_id=fetch_scanner.id
            )
        )
    )
    client.scans_api.launch(scan_id, ScanLaunchRequest())

    scan = client.scans_api.details(scan_id)

    wait_until(lambda: client.scans_api.details(scan_id),
               lambda details: details.info.status in
                               [Scan.STATUS_PENDING, Scan.STATUS_RUNNING, Scan.STATUS_INITIALIZING])
    assert scan.info.status in [Scan.STATUS_PENDING, Scan.STATUS_INITIALIZING, Scan.STATUS_RUNNING], \
        u'Scan is in launched state.'

    scan_details = wait_until(lambda: client.scans_api.details(scan_id),
                              lambda details: details.info.status in [Scan.STATUS_RUNNING])
    assert scan_details.info.status == Scan.STATUS_RUNNING, u'Scan should be running to test pause.'


    scan_list = client.scanners_api.get_scans(fetch_scanner.id)
    assert isinstance(scan_list, ScannerScanList), u'Get request returns type.'
    assert len(scan_list.scans) > 0, u'At least one test scan.'

    scan_uuid = scan.info.uuid
    test_scans = [s for s in scan_list.scans if s.id == scan_uuid]
    assert len(test_scans) == 1, u'Must contain test scan.'

    client.scanners_api.control_scans(fetch_scanner.id, scan_uuid, ScannerControlRequest(u'pause'))
    scan_details = wait_until(lambda: client.scans_api.details(scan_id),
                              lambda details: details.info.status in [Scan.STATUS_PAUSED])
    assert scan_details.info.status == Scan.STATUS_PAUSED, u'Scan is paused.'
