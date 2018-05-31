import os

from tenable_io.client import TenableIOClient


def example(test_file):

    # Generate unique name and file.
    test_json_file = test_file(u'example_export_%(chunk_id)s.json')

    '''
    Instantiate an instance of the TenableIOClient.
    '''
    client = TenableIOClient()

    '''
    Export and download vulnerabilities.
    Note: The file name can be optionally parameterized with "%(chunk_id)s" to allow multiple chunks. Otherwise the
        chunk ID will be append to the file name.
    '''
    chunks_available = client.export_helper.download_vulns(test_json_file)
    for chunk_id in chunks_available:
        chunk_file = test_json_file % {'chunk_id': chunk_id}
        assert os.path.isfile(chunk_file)
        os.remove(chunk_file)
