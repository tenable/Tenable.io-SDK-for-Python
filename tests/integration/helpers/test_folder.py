import pytest

from random import randint
from tenable_io.api.models import Folder

from tests.config import TenableIOTestConfig


def create_scan(client):
    return client.scan_helper.create(
        'test_scan_{}'.format(randint(0, 1000)),
        TenableIOTestConfig.get('scan_text_targets'),
        TenableIOTestConfig.get('scan_template_name')
    )


def create_folder(client):
    return client.folder_helper.create('test_folder_{}'.format(randint(0, 1000)))


@pytest.mark.vcr()
def test_folder_helper_default_folders(client):
    main_folder = client.folder_helper.main_folder()
    trash_folder = client.folder_helper.trash_folder()
    assert main_folder.type() == Folder.TYPE_MAIN, u'Correct folder type.'
    assert trash_folder.type() == Folder.TYPE_TRASH, u'Correct folder type.'


@pytest.mark.vcr()
def test_folder_helper_add_stop(client):
    scan = create_scan(client)
    folder = create_folder(client)
    assert scan.folder().id != folder.id, u'The scan is not in the folder already.'
    folder.add(scan)
    assert scan.folder().id == folder.id, u'The scan is in the folder.'
    scan.launch()
    assert not scan.stopped(), u'The scan is running.'
    folder.stop_scans()
    assert scan.stopped(), u'The scan is stopped.'
