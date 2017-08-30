import os

from datetime import datetime
from time import time

from tenable_io.api.models import Scan
from tenable_io.api.scans import ScanExportRequest
from tenable_io.client import TenableIOClient
from tenable_io.exceptions import TenableIOApiException


def example(test_name, test_file, test_targets):

    # Generate unique name and file.
    scan_name = test_name(u'example scan')
    test_nessus_file = test_file(u'example_report.nessus')
    test_pdf_file = test_file(u'example_report.pdf')

    '''
    Instantiate an instance of the TenableIOClient.
    '''
    client = TenableIOClient()

    '''
    Create a scan.
    '''
    scan = client.scan_helper.create(
        name=scan_name,
        text_targets=test_targets,
        template='basic'
    )
    assert scan.name() == scan_name

    '''
    Retrieve a scan by ID.
    '''
    scan_b = client.scan_helper.id(scan.id)
    assert scan_b is not scan
    assert scan_b.name() == scan_name

    '''
    Select scans by name.
    '''
    scans = client.scan_helper.scans(name=scan_name)
    assert scans[0].name() == scan_name

    '''
    Select scans by name with regular expression.
    '''
    scans = client.scan_helper.scans(name_regex=r'.*example scan.*')
    assert len(scans) > 0

    '''
    Launch a scan, then download when scan is completed.
    Note: The `download` method blocks until the scan is completed and the report is downloaded.
    '''
    scan.launch().download(test_pdf_file)
    assert os.path.isfile(test_pdf_file)
    os.remove(test_pdf_file)

    '''
    Launch a scan, pause it, resume it, then stop it.
    '''
    scan.launch().pause()
    assert scan.status() == Scan.STATUS_PAUSED
    scan.resume().stop()
    assert scan.status() == Scan.STATUS_CANCELED

    '''
    Stop a running scan if it does not complete within a specific duration.
    '''
    start = time()
    scan.launch().wait_or_cancel_after(10)
    assert time() - start >= 10

    '''
    Retrieve the history of a scan since a specific date or all.
    Note: The `since` argument is optional, all the history if omitted.
    '''
    histories = scan.histories(since=datetime(2016, 12, 1))
    assert len(histories) > 0

    '''
    Download the report for a specific scan in history.
    '''
    scan.download(test_pdf_file, history_id=histories[0].history_id)
    assert os.path.isfile(test_pdf_file)
    os.remove(test_pdf_file)

    '''
    Create a new scan by copying a scan.
    '''
    scan_copy = scan.copy()
    assert scan_copy.id != scan.id
    assert scan_copy.status() == Scan.STATUS_EMPTY

    '''
    Export a scan into a NESSUS file.
    '''
    scan.download(test_nessus_file, format=ScanExportRequest.FORMAT_NESSUS)
    assert os.path.isfile(test_nessus_file)

    '''
    Create a new scan by importing a NESSUS file.
    '''
    imported_scan = client.scan_helper.import_scan(test_nessus_file)
    assert imported_scan.details().info.name == scan.details().info.name
    os.remove(test_nessus_file)

    '''
    Stop all scans.
    Note: Use with caution as this will stop all ongoing scans (including any automated test).
    '''
    # client.scan_helper.stop_all()

    '''
    Check if a target has recently been scanned (including running scans).
    '''
    activities = client.scan_helper.activities(test_targets)
    last_history_id = scan.last_history().history_id
    assert [a for a in activities if last_history_id == a.history_id]

    '''
    Delete scans.
    '''
    scan.delete()
    scan_copy.delete()
    imported_scan.delete()

    try:
        scan.details()
        assert False
    except TenableIOApiException:
        pass
    try:
        scan_copy.details()
        assert False
    except TenableIOApiException:
        pass
    try:
        imported_scan.details()
        assert False
    except TenableIOApiException:
        pass
