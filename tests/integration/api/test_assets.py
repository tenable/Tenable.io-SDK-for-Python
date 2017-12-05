from tests.base import BaseTest

from tenable_io.api.models import AssetsAsset, AssetsAssetList, AssetsAssetSource
from tenable_io.exceptions import TenableIOErrorCode, TenableIOApiException


class TestAssetsApi(BaseTest):

    def test_assets(self, client):
        assets_list = client.assets_api.list()
        assert isinstance(assets_list, AssetsAssetList), u'Get request returns type.'

        for a in assets_list.assets:
            isinstance(a, AssetsAsset), u'Assets property represents type.'
            for s in a.sources:
                isinstance(s, AssetsAssetSource), u'Sources property represents type.'

    def test_asset(self, client):
        try:
            client.assets_api.get('test_assets_asset_info')
            assert False, u'TenableIOApiException should have been thrown for bad ID.'
        except TenableIOApiException as e:
            assert e.code is TenableIOErrorCode.BAD_REQUEST, u'Appropriate exception thrown.'
