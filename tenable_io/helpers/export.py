import tenable_io.util as util
from tenable_io.api.exports import VulnsRequestExportRequest
from tenable_io.api.models import VulnsExportStatus


class ExportHelper(object):

    def __init__(self, client):
        self._client = client

    def download_vulns(self, path, num_assets=None, severity=None, state=None, plugin_family=None, since=None,
                       file_open_mode='wb'):
        """Request the vulns export chunks, poll for status, and download them when it's available. The chunks will be
            downloaded in no particular order.

        :param path: The file path to save the report to.
        :param num_assets: Specifies the number of assets per exported chunk. Default is 50. Range is 50-5000. If you
            specify a value outside of that range, the system uses lower or upper bound value.
        :param severity: Defaults to all severity levels. Supported values are [info, low, medium, high,
            critical].
        :param state: The state of the vulnerabilities to include in the export. If not provided, default states are
            OPEN and REOPENED. Acceptable values are [OPEN, REOPENED, FIXED]. Case insensitive.
        :param plugin_family: The plugin family of the exported vulnerabilities. This filter is case sensitive.
        :param since: The start date (in Unix time) for the range of new or updated vulnerability data you want
            to export. If your request omits this parameter, exported data includes all vulnerabilities, regardless of
            date.
        :param file_open_mode: The open mode to the file output. Default to "wb".
        :return: The list of `chunk_id`s.
        """
        # If not parameterized for chunk ID.
        if path % {'chunk_id': 1} == path:
            path += '_%(chunk_id)s'

        export_uuid = self._client.exports_api.vulns_request_export(
            VulnsRequestExportRequest(
                num_assets=num_assets,
                filters={
                    u'severity': severity,
                    u'state': state,
                    u'plugin_family': plugin_family,
                    u'since': since
                }
            )
        )

        util.wait_until(
            lambda: self._client.exports_api.vulns_export_status(export_uuid).status ==
            VulnsExportStatus.STATUS_FINISHED)

        status = self._client.exports_api.vulns_export_status(export_uuid)

        # Download chunks
        for chunk_id in status.chunks_available:
            iter_content = self._client.exports_api.vulns_download_chunk(export_uuid, chunk_id)
            with open(path % {'chunk_id': chunk_id}, file_open_mode) as fd:
                for chunk in iter_content:
                    fd.write(chunk)

        return status.chunks_available
