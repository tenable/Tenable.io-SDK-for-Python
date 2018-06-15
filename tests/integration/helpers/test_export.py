import os

from tests.base import BaseTest


class TestExportHelper(BaseTest):

    def test_download_vulns(self, app, client):
        download_path = app.session_file_output('test_download_vulns_%(chunk_id)s_chunk')

        chunks_available = client.export_helper.download_vulns(download_path)
        for chunk_id in chunks_available:
            chunk_file = download_path % {'chunk_id': chunk_id}
            assert os.path.isfile(chunk_file), u'Chunk is downloaded with expected file name.'
            os.remove(chunk_file)

    def test_download_assets(self, app, client):
        download_path = app.session_file_output('test_download_assets_%(chunk_id)s_chunk')

        chunks_available = client.export_helper.download_assets(download_path, chunk_size=100)
        for chunk_id in chunks_available:
            chunk_file = download_path % {'chunk_id': chunk_id}
            assert os.path.isfile(chunk_file), u'Chunk is downloaded with expected file name.'
            os.remove(chunk_file)
