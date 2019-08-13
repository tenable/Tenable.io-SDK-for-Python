import os

from tenable_io.client import TenableIOClient
from tenable_io.api.models import AssetsExport, VulnsExport


def example():

    # Generate unique name and file.
    test_vulns_json_file = u'example_export_vulns_%(chunk_id)s.json'
    test_assets_json_file = u'example_export_assets_%(chunk_id)s.json'

    '''
    Instantiate an instance of the TenableIOClient.
    '''
    client = TenableIOClient()

    '''
    Export and load vulnerabilities to memory.
    '''
    vuln_list = client.export_helper.download_vulns()
    for vuln in vuln_list:
        assert isinstance(vuln, VulnsExport)

    '''
    Export and download vulnerabilities to disk.
    Note: The file name can be optionally parameterized with "%(chunk_id)s" to allow multiple chunks. Otherwise the
        chunk ID will be append to the file name.
    '''
    chunks_available = client.export_helper.download_vulns(path=test_vulns_json_file)
    for chunk_id in chunks_available:
        chunk_file = test_vulns_json_file % {'chunk_id': chunk_id}
        assert os.path.isfile(chunk_file)
        os.remove(chunk_file)

    '''
    Export and load assets to memory.
    '''
    asset_list = client.export_helper.download_assets()
    for asset in asset_list:
        assert isinstance(asset, AssetsExport)

    '''
    Export and download assets to disk.
    Note: The file name can be optionally parameterized with "%(chunk_id)s" to allow multiple chunks. Otherwise the
        chunk ID will be append to the file name.
    '''
    chunks_available = client.export_helper.download_assets(path=test_assets_json_file)
    for chunk_id in chunks_available:
        chunk_file = test_assets_json_file % {'chunk_id': chunk_id}
        assert os.path.isfile(chunk_file)
        os.remove(chunk_file)
