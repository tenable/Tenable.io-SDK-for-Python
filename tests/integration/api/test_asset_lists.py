import pytest

from tenable_io.api.asset_lists import AssetListCreateRequest
from tenable_io.api.models import AssetList, AssetListList
from tests.base import BaseTest


class TestAssetListsApi(BaseTest):

    @pytest.fixture(scope='class')
    def asset_list(self, app, client):
        asset_list = client.asset_lists_api.create(AssetListCreateRequest(
            name=app.session_name('test_asset_lists'),
            members='tenable.com',
            type='system',
        ))
        yield asset_list
        assert client.asset_lists_api.delete(asset_list.id), u'Asset list is deleted.'

    def test_list_return_correct_type(self, client):
        asset_list_list = client.asset_lists_api.list()
        assert isinstance(asset_list_list, AssetListList), u'The `list` method return type.'

    def test_create_delete(self, app, client):
        asset_list = client.asset_lists_api.create(AssetListCreateRequest(
            name=app.session_name('test_create_delete'),
            members='tenable.com',
            type='system',
        ))
        assert isinstance(asset_list, AssetList), u'The `create` method return type.'
        assert hasattr(asset_list, 'id'), u'Asset list has ID.'
        assert client.asset_lists_api.delete(asset_list.id), u'Asset list is deleted.'

    def test_get(self, asset_list, client):
        got_asset_list = client.asset_lists_api.details(asset_list.id)
        assert got_asset_list.id == asset_list.id, u'The `details` method returns asset list with matching ID.'

    def test_edit(self, app, client, asset_list):
        previous_name = asset_list.name
        new_name = app.session_name('test_edit')

        edited_asset_list = client.asset_lists_api.edit(AssetListCreateRequest(
            name=new_name,
            members=asset_list.members,
            type=asset_list.type,
        ), asset_list.id)
        assert edited_asset_list.name == new_name, u'The `edit` method returns asset list with matching name.'

        got_asset_list = client.asset_lists_api.details(edited_asset_list.id)
        assert got_asset_list.name == new_name, u'The `details` method returns asset list with matching name.'

        reverted_asset_list = client.asset_lists_api.edit(AssetListCreateRequest(
            name=previous_name,
            members=got_asset_list.members,
            type=got_asset_list.type,
        ), asset_list.id)
        assert reverted_asset_list.name == previous_name, u'The reverted asset list has matching name.'

    def test_list(self, client, asset_list):
        asset_list_list = client.asset_lists_api.list()
        for l in asset_list_list.asset_lists:
            assert isinstance(l, AssetList), u'Asset list list\'s element type.'
        assert len([l for l in asset_list_list.asset_lists if l.id == asset_list.id]) == 1, \
            u'Asset list list contains created access list.'
