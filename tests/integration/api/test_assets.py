import pytest

from tenable_io.api.models import AssetsAsset, AssetsAssetList, AssetsAssetSource


@pytest.mark.vcr()
def test_assets_list(client):
    assets_list = client.assets_api.list()
    assert isinstance(assets_list, AssetsAssetList), u'The `list` method did not return type `AssetsAssetList`.'


@pytest.mark.vcr()
def test_assets_get(client):
    assets_list = client.assets_api.list()
    assert len(assets_list.assets) > 0, u'Expected at least one asset.'
    asset = client.assets_api.get(assets_list.assets[0].id)
    assert isinstance(asset, AssetsAsset), u'The `get` method did not return type `AssetsAsset`.'
    for source in asset.sources:
        isinstance(source, AssetsAssetSource), u'Sources property did not represent correct type.'
