import pytest

from tenable_io.api.models import Folder

from tests.base import BaseTest
from tests.config import TenableIOTestConfig


class TestFolderHelper(BaseTest):

    @pytest.fixture(scope='class')
    def scan(self, app, client):
        """
        Create a scan for testing.
        """
        scan = client.scan_helper.create(
            app.session_name('test_folder'),
            TenableIOTestConfig.get('scan_text_targets'),
            TenableIOTestConfig.get('scan_template_name'))
        yield scan
        scan.delete()

    @pytest.fixture(scope='class')
    def folder(self, app, client):
        """
        Create a folder for testing.
        """
        folder = client.folder_helper.create(app.session_name('test_folder'))
        yield folder
        folder.delete()

    def test_default_folders(self, client):
        main_folder = client.folder_helper.main_folder()
        trash_folder = client.folder_helper.trash_folder()
        assert main_folder.type() == Folder.TYPE_MAIN, u'Correct folder type.'
        assert trash_folder.type() == Folder.TYPE_TRASH, u'Correct folder type.'

    def test_add_stop(self, folder, scan):
        assert scan.folder().id != folder.id, u'The scan is not in the folder already.'
        folder.add(scan)
        assert scan.folder().id == folder.id, u'The scan is in the folder.'
        scan.launch()
        assert not scan.stopped(), u'The scan is running.'
        folder.stop_scans()
        assert scan.stopped(), u'The scan is stopped.'
