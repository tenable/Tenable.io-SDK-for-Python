import os

from tenable_io.client import TenableIOClient


def example(test_file):

    test_asset_file = test_file(u'asset.nessus')
    test_vulnerability_file = test_file(u'vulnerability.nessus')

    date_range = 7

    '''
    Instantiate an instance of the TenableIOClient.
    '''
    client = TenableIOClient()

    '''
    Get recent assets in the past 7 days.
    Note: assets returns an iterator. An iterator that return pages of assets.
    '''
    assets_iter = client.workbench_helper.assets(date_range)
    assets = [a for page in assets_iter for a in page]

    '''
    Get recent vulnerabilities in the past 7 days.
    Note: vulnerabilities returns an iterator. An iterator that return pages of vulnerabilities.
    '''
    vulnerabilities_iter = client.workbench_helper.vulnerabilities(date_range)
    vulnerabilities = [v for page in vulnerabilities_iter for v in page]

    if len(vulnerabilities) < 1:
        return

    '''
    Get recent assets found for a plugin.
    '''
    plugin_id = vulnerabilities[0].plugin_id
    vulnerability_assets_iter = client.workbench_helper.assets(date_range, plugin_id=plugin_id)
    vulnerability_assets = [a for page in vulnerability_assets_iter for a in page]

    assert len(vulnerability_assets) > 0
    assert plugin_id in [v.plugin_id for v in vulnerability_assets[0].vulnerabilities]

    '''
    Get recent vulnerabilities found for an asset.
    '''
    asset_id = vulnerability_assets[0].asset.host_uuid
    asset_vulnerabilities_iter = client.workbench_helper.vulnerabilities(date_range, asset_id=asset_id)
    asset_vulnerabilities = [v for page in asset_vulnerabilities_iter for v in page]

    assert len(asset_vulnerabilities) > 0
    assert plugin_id in [v.plugin_id for v in asset_vulnerabilities]

    '''
    Export reports for a given asset or vulnerability.
    '''
    client.workbench_helper.export(test_asset_file, asset_id=assets[0].asset.host_uuid)
    client.workbench_helper.export(test_vulnerability_file, plugin_id=vulnerabilities[0].plugin_id)

    assert os.path.isfile(test_asset_file)
    assert os.path.isfile(test_vulnerability_file)
    os.remove(test_asset_file)
    os.remove(test_vulnerability_file)
