import pytest
import types


def get_asset(client):
    assets = next(client.workbench_helper.assets(30, page_size=0))
    return assets[0] if len(assets) > 0 else None

def get_vulnerability(client):
    vulnerabilities = next(client.workbench_helper.vulnerabilities(30, page_size=0))
    return vulnerabilities[0] if len(vulnerabilities) > 0 else None

@pytest.mark.vcr()
def test_workbench_helper_assets(client):
    assets_iter = client.workbench_helper.assets(30)
    assert isinstance(assets_iter, types.GeneratorType), u'Returns a generator.'
    assets_iter.close()


@pytest.mark.vcr()
def test_workbench_helper_vulnerabilities(client):
    vulnerabilities_iter = client.workbench_helper.vulnerabilities(30)
    assert isinstance(vulnerabilities_iter, types.GeneratorType), u'Returns a generator.'
    vulnerabilities_iter.close()


@pytest.mark.vcr()
def test_workbench_helper_assets_by_vulnerability_and_vulnerabilities_by_asset(client):
    vulnerability = get_vulnerability(client)
    # No vulnerability, no test.
    if vulnerability is not None:
        assets = next(client.workbench_helper.assets(30, plugin_id=vulnerability.plugin_id, page_size=0))
        assert len(assets) > 0, u'Should be at least one asset.'

        asset_id = assets[0].asset.host_uuid
        vulnerabilities = next(client.workbench_helper.vulnerabilities(30, asset_id=asset_id, page_size=0))
        assert len(vulnerabilities) > 0, u'Should be at least one vulnerability.'

        assert vulnerability.plugin_id in [v.plugin_id for v in vulnerabilities], \
            u'Vulnerability used to find the asset should be in this asset\'s list of vulnerabilities.'


@pytest.mark.vcr()
def test_workbench_helper_vulnerabilities_by_asset(client):
    asset = get_asset(client)
    # No asset, no test.
    if asset is not None:
        vulnerabilities = next(client.workbench_helper.vulnerabilities(
            30, asset_id=asset.asset.host_uuid, page_size=0))
        assert isinstance(vulnerabilities, list), u'Should be a list.'
