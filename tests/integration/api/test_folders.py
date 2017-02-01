import pytest

from tenable_io.api.models import FolderList
from tests.base import BaseTest


class TestFoldersApi(BaseTest):

    @pytest.fixture(scope='class')
    def folder_id(self, app, client):
        folder_id = client.folders_api.create(app.session_name('test_folders_0', length=5))
        yield folder_id
        assert client.folders_api.delete(folder_id), u'Folder is deleted.'

    def test_list(self, client):
        folder_list = client.folders_api.list()
        assert isinstance(folder_list, FolderList), u'The `list` method return type.'

    def test_create_delete(self, app, client):
        new_name = app.session_name('test_folders_1', length=5)
        folder_id = client.folders_api.create(new_name)
        new_folder = self._get_folder_from_folder_list(client, folder_id)

        assert new_folder.name == new_name, u'The newly created folder should be found in the list.'
        assert client.folders_api.delete(folder_id), u'The folder is deleted.'

    def test_edit(self, app, client, folder_id):
        test_folder = self._get_folder_from_folder_list(client, folder_id)
        assert test_folder, u'Test folder exists.'

        new_name = app.session_name('test_folders_2', length=5)
        old_name = test_folder.name

        client.folders_api.edit(test_folder.id, new_name)
        test_folder = self._get_folder_from_folder_list(client, folder_id)

        assert test_folder.name == new_name, u'The folder name returned should match the new name.'

        client.folders_api.edit(test_folder.id, old_name)
        test_folder = self._get_folder_from_folder_list(client, folder_id)

        assert test_folder.name == old_name, u'The returned folder name should match the previous folder name.'

    @staticmethod
    def _get_folder_from_folder_list(client, id):
        folder_list = client.folders_api.list()
        matching_folders = [f for f in folder_list.folders if f.id == id]
        return matching_folders[0] if len(matching_folders) > 0 else None
