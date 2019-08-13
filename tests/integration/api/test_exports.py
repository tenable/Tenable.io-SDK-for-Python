import pytest

from tenable_io.api.exports import ExportsAssetsRequest, ExportsVulnsRequest
from tenable_io.api.models import AssetsExport, ExportsAssetsStatus, ExportsVulnsStatus, VulnsExport
from tests.integration.api.utils.utils import wait_until


@pytest.mark.vcr()
def test_export_vulns(client):
    # Create export request
    export_uuid = client.exports_api.vulns_request_export(
        ExportsVulnsRequest(filters={'since': 1451606400})
    )
    assert export_uuid, u'The `vulns_request_export` method returns a valid export UUID'
    # Check status
    export_status = client.exports_api.vulns_export_status(export_uuid)
    assert isinstance(export_status, ExportsVulnsStatus), u'The `vulns_export_status` method return did not return type `ExportsVulnsStatus`.'

    wait_until(lambda: client.exports_api.vulns_export_status(export_uuid),
               lambda status: status.status == ExportsVulnsStatus.STATUS_FINISHED)
    export_status = client.exports_api.vulns_export_status(export_uuid)

    # Export results
    vuln_list = client.exports_api.vulns_chunk(export_uuid, export_status.chunks_available[0])
    for vuln in vuln_list:
        assert isinstance(vuln, VulnsExport), u'The list should only countain `VulnsExport` object type.'

@pytest.mark.vcr()
def test_export_assets(client):
    # Create export request
    export_uuid = client.exports_api.assets_request_export(
        ExportsAssetsRequest(chunk_size=100)
    )
    assert export_uuid, u'The `assets_request_export` method returns a valid export UUID'
    # Check status
    export_status = client.exports_api.assets_export_status(export_uuid)
    assert isinstance(export_status, ExportsAssetsStatus), u'The `assets_export_status` method return did not return type `ExportsAssetsStatus`.'

    wait_until(lambda: client.exports_api.assets_export_status(export_uuid),
               lambda status: status.status == ExportsAssetsStatus.STATUS_FINISHED)

    # Export results
    for chunk_id in export_status.chunks_available[:1]:
        asset_list = client.exports_api.assets_chunk(export_uuid, chunk_id)
        for asset in asset_list:
            assert isinstance(asset, AssetsExport), u'The list should only countain `AssetsExport` object type.'