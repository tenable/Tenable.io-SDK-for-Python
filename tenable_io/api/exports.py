from json import loads

from tenable_io.api.base import BaseApi, BaseRequest
from tenable_io.api.models import AssetsExport, ExportsAssetsStatus, ExportsVulnsStatus, VulnsExport
from tenable_io.util import payload_filter


class ExportsApi(BaseApi):

    def vulns_request_export(self, exports_vulns):
        """Export all vulnerabilities in the user's container that match the request criteria.

        :param exports_vulns: An instance of :class:`ExportsVulnsRequest`.
        :raise TenableIOApiException: When API error is encountered.
        :return: The export UUID.
        """
        response = self._client.post('vulns/export', payload=exports_vulns)
        return loads(response.text).get('export_uuid')

    def vulns_export_status(self, export_uuid):
        """Returns the status of your export request (QUEUED, PROCESSING, FINISHED, ERROR)
                Chunks are processed in parallel and may not complete in order.

        :param export_uuid: The export UUID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of `ExportsVulnsStatus`
        """
        response = self._client.get('vulns/export/%(export_uuid)s/status',
                                    path_params={'export_uuid': export_uuid})
        return ExportsVulnsStatus.from_json(response.text)

    def vulns_chunk(self, export_uuid, chunk_id):
        """Retrieve vulnerability chunk by ID.

        :param export_uuid: The export request UUID.
        :param chunk_id: The chunk ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: A list of :class:`tenable_io.api.models.VulnsExport` instances.
        """
        response = self._client.get('vulns/export/%(export_uuid)s/chunks/%(chunk_id)s',
                                    path_params={'export_uuid': export_uuid, 'chunk_id': chunk_id})
        return VulnsExport.from_json_list(response.text)

    def vulns_download_chunk(self, export_uuid, chunk_id, stream=True, chunk_size=1024):
        """Download vulnerability chunk by ID.

        :param export_uuid: The export request UUID.
        :param chunk_id: The chunk ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: The downloaded file.
        """
        response = self._client.get('vulns/export/%(export_uuid)s/chunks/%(chunk_id)s',
                                    path_params={'export_uuid': export_uuid, 'chunk_id': chunk_id},
                                    stream=stream)
        return response.iter_content(chunk_size=chunk_size)

    def assets_request_export(self, exports_assets):
        """Exports all assets in your container that match the request criteria.

        :param exports_assets: An instance of :class:`ExportsAssetsRequest`.
        :raise TenableIOApiException: When API error is encountered.
        :return: The UUID for the export request.
        """
        response = self._client.post('assets/export', payload=exports_assets)
        return loads(response.text).get('export_uuid')

    def assets_export_status(self, export_uuid):
        """Returns the status of your export request. Chunks are processed in serial and will complete in order.

        :param export_uuid: The UUID for the export request.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of `ExportsAssetsStatus`
        """
        response = self._client.get('assets/export/%(export_uuid)s/status',
                                    path_params={'export_uuid': export_uuid})
        return ExportsAssetsStatus.from_json(response.text)

    def assets_chunk(self, export_uuid, chunk_id):
        """Retrieve chunk by id. Chunks are available for export for up to 24 hours after they have been created. A
            404 is returned for expired chunks.

        :param export_uuid: The UUID for the export request.
        :param chunk_id: The ID of the asset chunk you want to export.
        :raise TenableIOApiException:  When API error is encountered.
        :return: A list of :class:`tenable_io.api.models.AssetsExport` instances.
        """
        response = self._client.get('assets/export/%(export_uuid)s/chunks/%(chunk_id)s',
                                    path_params={'export_uuid': export_uuid, 'chunk_id': chunk_id})
        return AssetsExport.from_json_list(response.text)

    def assets_download_chunk(self, export_uuid, chunk_id, stream=True, chunk_size=1024):
        """Download chunk by id. Chunks are available for download for up to 24 hours after they have been created. A
            404 is returned for expired chunks.

        :param export_uuid: The UUID for the export request.
        :param chunk_id: The ID of the asset chunk you want to export.
        :raise TenableIOApiException:  When API error is encountered.
        :return: The downloaded file.
        """
        response = self._client.get('assets/export/%(export_uuid)s/chunks/%(chunk_id)s',
                                    path_params={'export_uuid': export_uuid, 'chunk_id': chunk_id},
                                    stream=stream)
        return response.iter_content(chunk_size=chunk_size)


class ExportsAssetsRequest(BaseRequest):

    def __init__(self, chunk_size, filters=None):
        """Request for ExportApi.assets_request_export

        :param chunk_size: Specifies the number of assets per exported chunk. Range is 100-10000. If you specify a value
            outside of that range, a 400 error is returned.
        :type chunk_size: int
        :param filters: Specifies filters for exported assets. To return all assets, omit the filters object. If your
            request specifies multiple filters, the system combines the filters using the AND search operator.
        :type filters: dict
        :param filters.created_at: Returns all assets created later than the date specified. The specified date must be
            in the Unix timestamp format.
        :type filters.created_at: long
        :param filters.updated_at: Returns all assets updated later than the date specified. The specified date must be
            in the Unix timestamp format.
        :type filters.updated_at: long
        :param filters.terminated_at: Returns all assets terminated later than the date specified. The specified date
            must be in the Unix timestamp format.
        :type filters.terminated_at: long
        :param filters.deleted_at: Returns all assets deleted later than the date specified. The specified date must in
            the Unix timestamp format.
        :type filters.deleted_at: long
        :param filters.first_scan_time: Returns all assets with a first scan time later than the date specified. The
            specified date must be in the Unix timestamp format.
        :type filters.first_scan_time: long
        :param filters.last_authenticated_scan_time: Returns all assets with a last credentialed scan time later than
            the date specified. The specified date must be in the Unix timestamp format.
        :type filters.last_authenticated_scan_time: long
        :param filters.last_assessed: Returns all assets with a last assessed time later than the date specified. An
            asset is considered assessed if  it has been scanned by a credentialed or non-credentialed scan. The
            specified date must be in the Unix timestamp format.
        :type filters.last_assessed: long
        :param filters.servicenow_sysid: If true, returns all assets that have a ServiceNow Sys ID, regardless of value.
            If false, returns all assets that do not have a ServiceNow Sys ID.
        :type filters.servicenow_sysid: bool
        :param filters.sources: Returns assets that have the specified source. An asset source is the entity that
            reported the asset details. Sources can include sensors, connectors, and API imports. If your request
            specifies multiple sources, this request returns all assets that have been seen by any of the specified
            sources.
        :type filters.sources: list
        :param filters.has_plugin_results: If true, returns all assets that have plugin results. If false, returns all
            assets that do not have plugin results. An asset may not have plugin results if the asset details originated
            from a connector, an API import, or a discovery scan, rather than a vulnerabilities scan.
        :type filters.has_plugin_results: bool
        :param filters.tag.<category>: Returns all assets with the specified tags. The filter is defined as "tag",
            a period ("."), and the tag category name. The value of the filter is a list of tag values.
            ex. 'tag.City': ['Chicago', 'LA']
        :type filters.tag.<category>: list<str>
        """
        self.chunk_size = chunk_size
        self.filters = filters

    def as_payload(self, filter_=None):
        payload = super(ExportsAssetsRequest, self).as_payload(filter_)
        if u'filters' in payload:
            payload[u'filters'] = payload_filter(payload[u'filters'], filter_) or None
        return payload_filter(payload, filter_)


class ExportsVulnsRequest(BaseRequest):

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
        :type filters.since: int
        :param filters.tag.<category>: Returns all assets with the specified tags. The filter is defined as "tag",
            a period ("."), and the tag category name. The value of the filter is a list of tag values.
            ex. 'tag.City': ['Chicago', 'LA']
        :type filters.tag.<category>: list<str>
        :param cidr_range: Restricts search for vulnerabilities to assets assigned an IP address within the specified
            CIDR range. For example, 0.0.0.0/0 restricts the search to 0.0.0.1 and 255.255.255.254.
        :type filters.cidr_range: str
        :param first_found: The start date (in Unix time) for the range of vulnerability data you want to export,
            based on when a scan first found a vulnerability on an asset.
        :type filters.first_found: int
        :param last_found: The start date (in Unix time) for the range of vulnerability data you want to export,
            based on when a scan last found a vulnerability on an asset.
        :type filters.last_found: int
        :param last_fixed: The start date (in Unix time) for the range of vulnerability data you want to export,
            based on when the vulnerability state was changed to fixed.
        :type filters.last_fixed: int
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
        payload = super(ExportsVulnsRequest, self).as_payload(filter_)
        if u'filters' in payload:
            payload[u'filters'] = payload_filter(payload[u'filters'], filter_) or None
        return payload_filter(payload, filter_)
