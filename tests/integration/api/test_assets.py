import pytest

from tenable_io.api.assets import BulkACRRequest, BulkDeleteRequest, BulkMoveRequest
from tenable_io.api.models import AssetsAsset, AssetsAssetList, AssetsAssetDetails, AssetsAssetSource


@pytest.mark.vcr()
def test_assets_list(client):
    assets_list = client.assets_api.list()
    assert isinstance(assets_list, AssetsAssetList), u'The `list` method did not return type `AssetsAssetList`.'
    for asset in assets_list.assets:
        assert isinstance(asset, AssetsAsset)


@pytest.mark.vcr()
def test_assets_get(client):
    assets_list = client.assets_api.list()
    assert len(assets_list.assets) > 0, u'Expected at least one asset.'
    asset = client.assets_api.get(assets_list.assets[0].id)
    assert isinstance(asset, AssetsAssetDetails), u'The `get` method did not return type `AssetsAssetDetails`.'
    for source in asset.sources:
        isinstance(source, AssetsAssetSource), u'Sources property did not represent correct type.'


@pytest.mark.vcr()
def test_assets_bulk_move(client):
    assets_list = client.assets_api.list()
    networks = client.networks_api.list()
    asset = client.assets_api.get(assets_list.assets[0].id)
    networks = [network for network in networks.networks if network.uuid != asset.network_id[0]]
    req = BulkMoveRequest(source=asset.network_id[0], destination=networks[0].uuid, targets=asset.ipv4[0])
    resp = client.assets_api.bulk_move(req)
    assert isinstance(resp, int)
    assert resp == 1, u'Expected a single asset to be affected.'


@pytest.mark.vcr()
def test_assets_bulk_delete(client):
    assets_list = client.assets_api.list()
    asset = client.assets_api.get(assets_list.assets[0].id)
    req = BulkDeleteRequest(query={'field': 'ipv4', 'operator': 'eq', 'value': asset.ipv4[0]})
    resp = client.assets_api.bulk_delete(req)
    assert isinstance(resp, int)
    assert resp == 1, u'Expected a single asset to be affected.'


@pytest.mark.vcr()
def test_assets_update_acr(client):
    assets_list = client.assets_api.list()
    asset = client.assets_api.get(assets_list.assets[0].id)
    req = BulkACRRequest(acr_score=9, reason=[BulkACRRequest.REASON_DEV_ONLY], note='Internal', asset=[asset.id])
    assert client.assets_api.update_acr(req)

