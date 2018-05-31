import os

from tenable_io.api.exports import VulnsRequestExportRequest
from tenable_io.api.models import VulnsExportStatus
from tests.base import BaseTest


class TestExportsApi(BaseTest):

    def test_vulns_export_status_download(self, app, client):
        export_uuid = client.exports_api.vulns_request_export(
            VulnsRequestExportRequest()
        )
        assert export_uuid, u'The `vulns_request_export` method returns a valid export UUID'

        export_status = client.exports_api.vulns_export_status(export_uuid)
        assert isinstance(export_status, VulnsExportStatus), u'The `vulns_export_status` method returns type.'

        self.wait_until(lambda: client.exports_api.vulns_export_status(export_uuid),
                        lambda status: status.status == VulnsExportStatus.STATUS_FINISHED)

        export_status = client.exports_api.vulns_export_status(export_uuid)
        assert export_status.status == VulnsExportStatus.STATUS_FINISHED, u'Export chunks are ready.'

        for chunk_id in export_status.chunks_available[:1]:
            iter_content = client.exports_api.vulns_download_chunk(export_uuid, chunk_id, False)
            download_path = app.session_file_output('test_vulns_export_status_download')
            assert not os.path.isfile(download_path), u'Chunk does not yet exist.'

            with open(download_path, 'wb') as fd:
                for chunk in iter_content:
                    fd.write(chunk)
            assert os.path.isfile(download_path), u'Export chunk is downloaded.'
            assert os.path.getsize(download_path) > 0, u'Export chunk is not empty.'
            os.remove(download_path)
