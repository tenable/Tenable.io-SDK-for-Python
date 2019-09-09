import pytest

from tenable_io.api.models import FolderList


@pytest.mark.vcr()
def test_folders_create(new_folder):
    assert isinstance(new_folder, int), u'The `create` method did not return type `int`.'


@pytest.mark.vcr()
def test_folders_list(client):
    folder_list = client.folders_api.list()
    assert isinstance(folder_list, FolderList), u'The `list` method did not return type `FolderList`.'


@pytest.mark.vcr()
def test_folders_delete(client, new_folder):
    assert client.folders_api.delete(new_folder), u'The folder was not deleted.'


@pytest.mark.vcr()
def test_folders_edit(client, new_folder):
    folder_id = new_folder
    assert client.folders_api.edit(folder_id, 'folder_name_edit'), u'The folder was not edited.'

    folder_list = client.folders_api.list()
    edited_folder = [f for f in folder_list.folders if f.id == folder_id]
    assert edited_folder[0].name == 'folder_name_edit', u'The returned folder name should match the the edited value.'
