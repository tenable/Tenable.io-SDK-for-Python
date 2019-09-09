import os
import pytest

from tenable_io.api.models import Asset, AssetActivity, AssetActivityList, AssetList, AssetInfo, Vulnerability, \
    VulnerabilityList, VulnerabilityOutputList
from tenable_io.api.workbenches import WorkbenchesApi

from tests.integration.api.utils.utils import wait_until


@pytest.mark.vcr()
def test_workbenches_assets(client):
    assets_list = client.workbenches_api.assets()
    assert isinstance(assets_list, AssetList), u'The `assets` method did not return type `AssetList`.'
    for asset in assets_list.assets:
        assert isinstance(asset, Asset), u'Expected a list of type `Asset`.'


@pytest.mark.vcr()
def test_workbenches_assets_vulnerabilities(client):
    assets_list = client.workbenches_api.assets_vulnerabilities()
    assert isinstance(assets_list, AssetList), u'The `assets_vulnerabilities` method did not return type `AssetList`.'


@pytest.mark.vcr()
def test_workbenches_asset_activity(client, fetch_asset):
    asset_activity = client.workbenches_api.asset_activity(fetch_asset.id)
    assert isinstance(asset_activity, AssetActivityList), \
        u'The `asset_activity` method did not return type `AssetActivityList`.'
    for activity in asset_activity.activity:
        assert isinstance(activity, AssetActivity), u'Expected a list of type `AssetActivity`.'


@pytest.mark.vcr()
def test_workbenches_asset_info(client, fetch_asset):
    asset_info = client.workbenches_api.asset_info(fetch_asset.id)
    assert isinstance(asset_info, AssetInfo), u'The `asset_info` method did not return type `AssetInfo`.'


@pytest.mark.vcr()
def test_workbenches_asset_vulnerabilities(client, fetch_asset):
    asset_vulns = client.workbenches_api.asset_vulnerabilities(fetch_asset.id)
    assert isinstance(asset_vulns, VulnerabilityList), \
        u'The `asset_vulnerabilities` method did not return type `VulnerabilityList`.'


@pytest.mark.vcr()
def test_workbenches_asset_vulnerabilities(client, fetch_asset):
    asset_vulns = client.workbenches_api.asset_vulnerabilities(fetch_asset.id)
    assert isinstance(asset_vulns, VulnerabilityList), \
        u'The `asset_vulnerabilities` method did not return type `VulnerabilityList`.'


@pytest.mark.vcr()
def test_workbenches_vulnerabilities(client):
    vulnerabilities_list = client.workbenches_api.vulnerabilities()
    assert isinstance(vulnerabilities_list, VulnerabilityList), \
        u'The `vulnerabilities` method did not return type `VulnerabilityList`.'
    for vulnerability in vulnerabilities_list.vulnerabilities:
        assert isinstance(vulnerability, Vulnerability), u'Expected a list of type `Vulnerability`.'


@pytest.mark.vcr()
def test_workbenches_vulnerability_output(client, fetch_vulnerability):
    vulnerability_output = client.workbenches_api.vulnerability_output(fetch_vulnerability.plugin_id)
    assert isinstance(vulnerability_output, VulnerabilityOutputList), \
        u'The `vulnerability_output` method did not return type `VulnerabilityOutputList`.'


@pytest.mark.vcr()
def test_workbenches_export(client):
    file_id = client.workbenches_api.export_request(
        WorkbenchesApi.FORMAT_NESSUS,
        WorkbenchesApi.REPORT_VULNERABILITIES,
        WorkbenchesApi.CHAPTER_VULN_BY_ASSET,
    )
    assert file_id, u'The `export_request` method did not return a valid file ID.'

    export_status = wait_until(lambda: client.workbenches_api.export_status(file_id),
                                    lambda status: status == WorkbenchesApi.STATUS_EXPORT_READY)

    assert export_status == WorkbenchesApi.STATUS_EXPORT_READY, u'Workbench export is not ready.'

    iter_content = client.workbenches_api.export_download(file_id, False)
    download_path = 'test_workbench_export'

    assert not os.path.isfile(download_path), u'Workbench report does not exist.'

    with open(download_path, 'wb') as fd:
        for chunk in iter_content:
            fd.write(chunk)
    assert os.path.isfile(download_path), u'Workbench report was not downloaded.'
    assert os.path.getsize(download_path) > 0, u'Workbench report is empty.'

    os.remove(download_path)
