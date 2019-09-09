import pytest

import os

from tenable_io.api.models import AssetsExport, VulnsExport


@pytest.mark.vcr()
def test_export_helper_get_vulns(client):
    vuln_list = client.export_helper.download_vulns()
    for vuln in vuln_list:
        assert isinstance(vuln, VulnsExport), u'The list of `VulnsExport` object type.'


@pytest.mark.vcr()
def test_export_helper_download_vulns(client):
    download_path = 'test_download_vulns_%(chunk_id)s_chunk'

    chunks_available = client.export_helper.download_vulns(path=download_path)
    for chunk_id in chunks_available:
        chunk_file = download_path % {'chunk_id': chunk_id}
        assert os.path.isfile(chunk_file), u'Chunk is downloaded with expected file name.'
        os.remove(chunk_file)


@pytest.mark.vcr()
def test_export_helper_get_assets(client):
    asset_list = client.export_helper.download_assets()
    for asset in asset_list:
        assert isinstance(asset, AssetsExport), u'The list of `AssetsExport` object type.'


@pytest.mark.vcr()
def test_export_helper_download_assets(client):
    download_path = 'test_download_assets_%(chunk_id)s_chunk'

    chunks_available = client.export_helper.download_assets(path=download_path)
    for chunk_id in chunks_available:
        chunk_file = download_path % {'chunk_id': chunk_id}
        assert os.path.isfile(chunk_file), u'Chunk is downloaded with expected file name.'
        os.remove(chunk_file)
