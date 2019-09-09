import os
import pytest

from time import time
from random import randint

from tenable_io.api.scans import ScanExportRequest
from tests.config import TenableIOTestConfig


def create_scan(client):
    """
    Create a scan for testing.
    """
    return client.scan_helper.create(
        'test_scan_{}'.format(randint(0, 1000)),
        TenableIOTestConfig.get('scan_text_targets'),
        TenableIOTestConfig.get('scan_template_name')
    )


@pytest.mark.vcr()
def test_scan_helper_details(client):
    scan = create_scan(client)
    scan_detail = scan.details()
    assert scan_detail.info.object_id == scan.id, u'ScanRef `id` should match ID in ScanDetail.'


@pytest.mark.skip(reason="CI-16072 & CI-15053")
@pytest.mark.vcr()
def test_scan_helper_alt_target_launch_stop_download_import(client):
    scan = create_scan(client)
    download_path = 'test_scan_launch_download'

    assert not os.path.isfile(download_path), u'Scan report does not yet exist.'

    alt_targets = [TenableIOTestConfig.get('scan_alt_targets')]
    histories = scan.launch(wait=True, alt_targets=alt_targets).stop()\
        .download(download_path, format=ScanExportRequest.FORMAT_NESSUS).histories()

    assert histories[0].alt_targets_used is True, u'Alternative target used in scan'
    assert os.path.isfile(download_path), u'Scan report is downloaded.'

    imported_scan = client.scan_helper.import_scan(download_path)
    assert imported_scan.details().info.name == scan.details().info.name, \
        u'Imported scan retains name of exported scan.'

    imported_scan.delete()

    os.remove(download_path)
    assert not os.path.isfile(download_path), u'Scan report is deleted.'


@pytest.mark.vcr()
def test_scan_helper_cancel_after(client):
    scan = create_scan(client)
    cancel_after_seconds = 10

    start_time = time()
    scan.launch().wait_or_cancel_after(cancel_after_seconds)
    stop_time = time()

    assert stop_time - start_time >= cancel_after_seconds, \
        u'Scan is ran for at least %s seconds.' % cancel_after_seconds
    assert scan.stopped(), u'Scan is stopped.'


@pytest.mark.vcr()
def test_scan_helper_return_last_history(client):
    scan = create_scan(client)
    for _ in range(2):
        scan.launch().wait_or_cancel_after(10)
        assert scan.stopped(), u'Scan is stopped.'
    scan_histories = scan.histories()
    most_recent_history = scan.last_history()
    assert max([h.history_id for h in scan_histories]) == most_recent_history.history_id, \
        u'last_history should return the most recent history.'
    assert max([h.last_modification_date for h in scan_histories]) == most_recent_history.last_modification_date, \
        u'last_history should return the most recent history.'


@pytest.mark.skip()
@pytest.mark.vcr()
def test_scan_helper_activities(client):
    scan = create_scan(client)
    scan_targets = TenableIOTestConfig.get('scan_text_targets')
    scan.launch().pause()
    history_id = scan.last_history().history_id

    activities = client.scan_helper.activities([scan_targets], date_range=1)

    activity = next((a for a in activities if a.history_id == history_id), None)
    assert activity, u'Uncompleted scan history should be in activities.'
    assert activity.timestamp is None, u'Uncompleted scan activity has no timestamp.'

    scan.resume().wait_or_cancel_after(10)

    activities = client.scan_helper.activities([scan_targets], date_range=1)
    activity = next((a for a in activities if a.history_id == history_id), None)
    assert activity is not None, u'Completed scan history should be in activities.'
    assert activity.timestamp is not None, u'Completed scan activity has a timestamp.'
