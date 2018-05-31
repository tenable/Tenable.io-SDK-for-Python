from json import loads

from tenable_io.api.base import BaseApi, BaseRequest
from tenable_io.api.models import VulnsExportStatus
from tenable_io.util import payload_filter


class ExportsApi(BaseApi):

    def vulns_request_export(self, vulns_request_export):
        """Export all vulnerabilities in the user's container that match the request criteria.

        :param vulns_request_export: An instance of :class:`VulnsRequestExportRequest`.
        :raise TenableIOApiException: When API error is encountered.
        :return: The export uuid
        """
        response = self._client.post('vulns/export', payload=vulns_request_export)
        return loads(response.text).get('export_uuid')

    def vulns_export_status(self, export_uuid):
        """Returns the status of your export request (QUEUED, PROCESSING, FINISHED, ERROR)
                Chunks are processed in parallel and may not complete in order.

        :param export_uuid: The export uuid
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of `VulnsExportStatus`
        """
        response = self._client.get('vulns/export/%(export_uuid)s/status',
                                    path_params={'export_uuid': export_uuid})
        return VulnsExportStatus.from_json(response.text)

    def vulns_download_chunk(self, export_uuid, chunk_id, stream=True, chunk_size=1024):
        """Download vulnerability chunk by id.

        :param export_uuid: The export request uuid
        :param chunk_id: The chunk id
        :raise TenableIOApiException:  When API error is encountered.
        :return: The downloaded file.
        """
        response = self._client.get('vulns/export/%(export_uuid)s/chunks/%(chunk_id)s',
                                    path_params={'export_uuid': export_uuid, 'chunk_id': chunk_id},
                                    stream=stream)
        return response.iter_content(chunk_size=chunk_size)


class VulnsRequestExportRequest(BaseRequest):

    FILTERS_SEVERITIES = [u'info', u'low', u'medium', u'high', u'critical']
    FILTERS_STATES = [u'open', u'reopened', u'fixed']

    def __init__(self, num_assets=None, filters=None):
        """Request for ExportApi.vulns_request_export

        :param num_assets: Specifies the number of assets per exported chunk. Default is 50. Range is 50-5000. If you
            specify a value outside of that range, the system uses lower or upper bound value.
        :type num_assets: int
        :param filters.severity: Defaults to all severity levels. Supported values are [info, low, medium, high,
            critical].
        :type filters.severity: list
        :param filters.state: The state of the vulnerabilities to include in the export. If not provided, default states
            are OPEN and REOPENED. Acceptable values are [OPEN, REOPENED, FIXED]. Case insensitive.
        :type filters.state: list
        :param filters.plugin_family: The plugin family of the exported vulnerabilities. This filter is case sensitive.
        :type filters.plugin_family: list
        :param filters.since: The start date (in Unix time) for the range of new or updated vulnerability data you want
            to export. If your request omits this parameter, exported data includes all vulnerabilities, regardless of
            date.
        :type filters.since: long
        """
        if filters and u'severity' in filters and filters[u'severity']:
            for severity in filters[u'severity']:
                assert severity in self.FILTERS_SEVERITIES

        if filters and u'state' in filters and filters[u'state']:
            for state in filters[u'state']:
                assert state.lower() in self.FILTERS_STATES

        self.num_assets = num_assets
        self.filters = filters

    def as_payload(self, filter_=None):
        payload = super(VulnsRequestExportRequest, self).as_payload(filter_)
        if u'filters' in payload:
            payload[u'filters'] = payload_filter(payload[u'filters'], filter_) or None
        return payload_filter(payload, filter_)
