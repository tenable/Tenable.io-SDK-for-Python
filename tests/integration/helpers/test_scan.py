import os
import pytest
from time import time

from tenable_io.api.scans import ScanExportRequest

from tests.base import BaseTest
from tests.config import TenableIOTestConfig


class TestScanHelper(BaseTest):

    @pytest.fixture(scope='class')
    def scan(self, app, client):
        """
        Create a scan for testing.
        """
        scan = client.scan_helper.create(
            app.session_name('test_scan'),
            TenableIOTestConfig.get('scan_text_targets'),
            TenableIOTestConfig.get('scan_template_name'))
        yield scan
        scan.delete()

    def test_details(self, scan):
        scan_detail = scan.details()
        assert scan_detail.info.object_id == scan.id, u'ScanRef `id` should match ID in ScanDetail.'

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
