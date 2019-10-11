import tenable_io.util as util
from tenable_io.api.exports import ExportsAssetsRequest, ExportsVulnsRequest
from tenable_io.api.models import ExportsAssetsStatus, ExportsVulnsStatus


class ExportHelper(object):

    def __init__(self, client):
        self._client = client

    def download_vulns(self, path=None, num_assets=50, severity=None, state=None, plugin_family=None, since=None,
                       tags=None, cidr_range=None, first_found=None, last_found=None, last_fixed=None,
                       file_open_mode='wb'):
        """Request the vulns export chunks, poll for status, and download them to disk or load to memory when it's
            available. The chunks will be retrieved in no particular order.

        :param path: The file path to save the report to. Will load to memory if equals `None`
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
        :param tags: Returns all assets with the specified tags. The filter is defined as a dict with catgeory name as
            the key and a list of values as the value. Ex: {tag_category_name:[tag_value(s)]}
        :param cidr_range: Restricts search for vulnerabilities to assets assigned an IP address within the specified
            CIDR range. For example, 0.0.0.0/0 restricts the search to 0.0.0.1 and 255.255.255.254.
        :param first_found: The start date (in Unix time) for the range of vulnerability data you want to export,
            based on when a scan first found a vulnerability on an asset.
        :param last_found: The start date (in Unix time) for the range of vulnerability data you want to export,
            based on when a scan last found a vulnerability on an asset.
        :param last_fixed: 	The start date (in Unix time) for the range of vulnerability data you want to export,
            based on when the vulnerability state was changed to fixed.
        :param file_open_mode: The open mode to the file output. Default to "wb".
        :return: The list of `chunk_id`s.
        """
        # If not parameterized for chunk ID.
        if path is not None and path % {'chunk_id': 1} == path:
            path += '_%(chunk_id)s'

        filters = {
                    u'severity': severity,
                    u'state': state,
                    u'plugin_family': plugin_family,
                    u'since': since,
                    u'cidr_range': cidr_range,
                    u'first_found': first_found,
                    u'last_found': last_found,
                    u'last_fixed': last_fixed
                }

        # Parse tag filters
        if tags is not None:
            tags = {u'tag.{}'.format(k): v for k, v in tags.items()}
            filters.update(tags)

        export_uuid = self._client.exports_api.vulns_request_export(
            ExportsVulnsRequest(
                num_assets=num_assets,
                filters=filters
            )
        )

        util.wait_until(
            lambda: self._client.exports_api.vulns_export_status(export_uuid).status ==
            ExportsVulnsStatus.STATUS_FINISHED)

        status = self._client.exports_api.vulns_export_status(export_uuid)

        # Retrieve chunks
        vulns = []
        for chunk_id in status.chunks_available:
            if path is None:
                vulns += self._client.exports_api.vulns_chunk(export_uuid, chunk_id)
            else:
                iter_content = self._client.exports_api.vulns_download_chunk(export_uuid, chunk_id)
                with open(path % {'chunk_id': chunk_id}, file_open_mode) as fd:
                    for chunk in iter_content:
                        fd.write(chunk)

        return vulns if path is None else status.chunks_available

    def download_assets(self, path=None, chunk_size=100, created_at=None, updated_at=None, terminated_at=None,
                        deleted_at=None, first_scan_time=None, last_authenticated_scan_time=None, last_assessed=None,
                        servicenow_sysid=None,  sources=None, has_plugin_results=None, tags=None, file_open_mode='wb'):
        """Request the vulns export chunks, poll for status, and download them when it's available. The chunks will be
            retrieved in no particular order.

        :param path: The file path to save the report to. Will load in memory if equals `None`
        :param chunk_size: Specifies the number of assets per exported chunk. Default is 100. Range is 100-10000. If you
            specify a value outside of that range, a 400 error is returned.
        :param created_at: Returns all assets created later than the date specified. The specified date must be in the
            Unix timestamp format.
        :param updated_at: Returns all assets updated later than the date specified. The specified date must be in the
            Unix timestamp format.
        :param terminated_at: Returns all assets terminated later than the date specified. The specified date must be in
            the Unix timestamp format.
        :param deleted_at: Returns all assets deleted later than the date specified. The specified date must in the Unix
            timestamp format.
        :param first_scan_time: Returns all assets with a first scan time later than the date specified. The specified
            date must be in the Unix timestamp format.
        :param last_authenticated_scan_time: Returns all assets with a last credentialed scan time later than the date
            specified. The specified date must be in the Unix timestamp format.
        :param last_assessed: Returns all assets with a last assessed time later than the date specified. An asset is
            considered assessed if  it has been scanned by a credentialed or non-credentialed scan. The specified date
            must be in the Unix timestamp format.
        :param servicenow_sysid: If true, returns all assets that have a ServiceNow Sys ID, regardless of value. If
            false, returns all assets that do not have a ServiceNow Sys ID.
        :param sources: Returns assets that have the specified source. An asset source is the entity that reported the
            asset details. Sources can include sensors, connectors, and API imports. If your request specifies multiple
            sources, this request returns all assets that have been seen by any of the specified sources.
        :param has_plugin_results: If true, returns all assets that have plugin results. If false, returns all assets
            that do not have plugin results. An asset may not have plugin results if the asset details originated from a
            connector, an API import, or a discovery scan, rather than a vulnerabilities scan.
        :param tags: Returns all assets with the specified tags. The filter is defined as a dict with catgeory name as
            the key and a list of values as the value. Ex: {tag_category_name:[tag_value(s)]}
        :param file_open_mode: The open mode to the file output. Default to "wb".
        :return: The list of exported assets if path is `None` else the list of `chunk_id`s.
        """
        # If not parameterized for chunk ID.
        if path is not None and path % {'chunk_id': 1} == path:
            path += '_%(chunk_id)s'

        filters = {
                    u'created_at': created_at,
                    u'updated_at': updated_at,
                    u'terminated_at': terminated_at,
                    u'deleted_at': deleted_at,
                    u'first_scan_time': first_scan_time,
                    u'last_authenticated_scan_time': last_authenticated_scan_time,
                    u'last_assessed': last_assessed,
                    u'servicenow_sysid': servicenow_sysid,
                    u'sources': sources,
                    u'has_plugin_results': has_plugin_results
                }

        # Parse tag filters
        if tags is not None:
            tags = {u'tag.{}'.format(k): v for k, v in tags.items()}
            filters.update(tags)

        export_uuid = self._client.exports_api.assets_request_export(
            ExportsAssetsRequest(
                chunk_size=chunk_size,
                filters=filters
            )
        )

        util.wait_until(
            lambda: self._client.exports_api.assets_export_status(export_uuid).status ==
            ExportsAssetsStatus.STATUS_FINISHED)

        status = self._client.exports_api.assets_export_status(export_uuid)

        # Download chunks
        assets = []
        for chunk_id in status.chunks_available:
            if path is None:
                assets += self._client.exports_api.assets_chunk(export_uuid, chunk_id)
            else:
                iter_content = self._client.exports_api.assets_download_chunk(export_uuid, chunk_id)
                with open(path % {'chunk_id': chunk_id}, file_open_mode) as fd:
                    for chunk in iter_content:
                        fd.write(chunk)

        return assets if path is None else status.chunks_available
