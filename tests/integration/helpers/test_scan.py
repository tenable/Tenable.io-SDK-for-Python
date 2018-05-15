import os
import pytest
from time import time

from tenable_io.api.scans import ScanExportRequest

from tests.base import BaseTest
from tests.config import TenableIOTestConfig


class TestScanHelper(BaseTest):

    @pytest.fixture(scope='class')
    def scan_targets(self):
        """
        Define a scan_targets
        """
        yield TenableIOTestConfig.get('scan_text_targets')

    @pytest.fixture(scope='class')
    def scan(self, app, client, scan_targets):
        """
        Create a scan for testing.
        """
        scan = client.scan_helper.create(
            app.session_name('test_scan'),
            scan_targets,
            TenableIOTestConfig.get('scan_template_name'))
        yield scan
        scan.delete(force_stop=True)

    def test_details(self, scan):
        scan_detail = scan.details()
        assert scan_detail.info.object_id == scan.id, u'ScanRef `id` should match ID in ScanDetail.'

    @pytest.mark.skip(reason="CI-16072 & CI-15053")
    def test_alt_target_launch_stop_download_import(self, app, client, scan):
        download_path = app.session_file_output('test_scan_launch_download')

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

    def test_cancel_after(self, scan):
        cancel_after_seconds = 10

        start_time = time()
        scan.launch().wait_or_cancel_after(cancel_after_seconds)
        stop_time = time()

        assert stop_time - start_time >= cancel_after_seconds, \
            u'Scan is ran for at least %s seconds.' % cancel_after_seconds
        assert scan.stopped(), u'Scan is stopped.'

    def test_return_last_history(self, scan):
        for _ in range(5):
            scan.launch().wait_or_cancel_after(10)
            assert scan.stopped(), u'Scan is stopped.'
        scan_histories = scan.histories()
        most_recent_history = scan.last_history()
        assert max([h.history_id for h in scan_histories]) == most_recent_history.history_id, \
            u'last_history should return the most recent history.'
        assert max([h.last_modification_date for h in scan_histories]) == most_recent_history.last_modification_date, \
            u'last_history should return the most recent history.'

    @pytest.mark.xfail(reason="CI-16090")
    def test_activities(self, client, scan, scan_targets):
        scan.launch().pause()
        history_id = scan.last_history().history_id

        activities = client.scan_helper.activities([scan_targets], date_range=1)

        activity = next((a for a in activities if a.history_id == history_id), None)
        assert activity, u'Uncompleted scan history should be in activities.'
        assert activity.timestamp is None, u'Uncompleted scan activity has no timestamp.'

        scan.resume().wait_until_stopped()

        activities = client.scan_helper.activities([scan_targets], date_range=1)
        activity = next((a for a in activities if a.history_id == history_id), None)
        assert activity, u'Completed scan history should be in activities.'
        assert activity.timestamp is not None, u'Completed scan activity has a timestamp.'
