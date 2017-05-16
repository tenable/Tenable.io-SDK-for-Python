from json import loads

from tenable_io.api.base import BaseApi
from tenable_io.api.models import AssetActivityList, AssetList, AssetInfo, VulnerabilityList, \
    VulnerabilityOutputList


class WorkbenchesApi(BaseApi):

    CHAPTER_EXEC_SUMMARY = u'exec_summary'
    CHAPTER_VULN_BY_ASSET = u'vuln_by_asset'
    CHAPTER_VULN_BY_PLUGIN = u'vuln_by_plugin'
    CHAPTER_VULN_HOSTS_SUMMARY = u'vuln_hosts_summary'

    FILTER_TYPE_AND = u'and'
    FILTER_TYPE_OR = u'or'

    FORMAT_CSV = u'csv'
    FORMAT_HTML = u'html'
    FORMAT_NESSUS = u'nessus'
    FORMAT_PDF = u'pdf'

    REPORT_VULNERABILITIES = u'vulnerabilities'

    STATUS_EXPORT_READY = u'ready'

    def assets(self, date_range=None, filters=None, filter_search_type=None):
        """List all the assets recorded.

        :param date_range: The number of days of data prior to and including today that should be returned.
        :param filters: An array containing filters to apply to the exported scan report.
        :param filter_search_type: The type of search to be used. Can have a value of **and**(default) or **or**.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`AssetList`.
        """
        params = {'date_range': date_range, 'filter': filters, 'filter.search_type': filter_search_type}
        response = self._client.get('workbenches/assets',
                                    params={k: v for (k, v) in params.items() if v})
        return AssetList.from_json(response.text)

    def assets_vulnerabilities(self, date_range=None, filters=None, filter_search_type=None):
        """List all the assets with vulnerabilities.

        :param date_range: The number of days of data prior to and including today that should be returned.
        :param filters: An array containing filters to apply to the exported scan report.
        :param filter_search_type: The type of search to be used. Can have a value of **and**(default) or **or**.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`AssetList`.
        """
        params = {'date_range': date_range, 'filter': filters, 'filter.search_type': filter_search_type}
        response = self._client.get('workbenches/assets/vulnerabilities',
                                    params={k: v for (k, v) in params.items() if v})
        return AssetList.from_json(response.text)

    def asset_activity(self, asset_id):
        """List detailed info of an asset.

        :param asset_id: The asset ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`AssetInfo`.
        """
        response = self._client.get('workbenches/assets/%(asset_id)s/activity',
                                    path_params={'asset_id': asset_id})
        return AssetActivityList.from_json(response.text)

    def asset_info(self, asset_id):
        """List detailed info of an asset.

        :param asset_id: The asset ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`AssetInfo`.
        """
        response = self._client.get('workbenches/assets/%(asset_id)s/info',
                                    path_params={'asset_id': asset_id})
        return AssetInfo.from_dict(loads(response.text).get('info'))

    def asset_vulnerabilities(self, asset_id, date_range=None, filters=None, filter_search_type=None):
        """List all the vulnerabilities recorded for a given asset.

        :param asset_id: The asset ID.
        :param date_range: The number of days of data prior to and including today that should be returned.
        :param filters: An array containing filters to apply to the exported scan report.
        :param filter_search_type: The type of search to be used. Can have a value of **and**(default) or **or**.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`VulnerabilityList`.
        """
        params = {'date_range': date_range, 'filter': filters, 'filter.search_type': filter_search_type}
        response = self._client.get('workbenches/assets/%(asset_id)s/vulnerabilities',
                                    params={k: v for (k, v) in params.items() if v},
                                    path_params={'asset_id': asset_id})
        return VulnerabilityList.from_json(response.text)

    def export_download(self, file_id, stream=True, chunk_size=1024):
        """Download a file that has been prepared for export.

        :param file_id: The unique identifier of the workbench report being downloaded.
        :param stream: Default to True. If False, the response content will be immediately downloaded.
        :param chunk_size: If Stream=False, data is returned as a single chunk.
            If Stream=True, it's the number of bytes it should read into memory.
        :raise TenableIOApiException:  When API error is encountered.
        :return: The content iterator for the file.
        """
        response = self._client.get('workbenches/export/%(file_id)s/download',
                                    path_params={'file_id': file_id},
                                    stream=stream)
        return response.iter_content(chunk_size=chunk_size)

    def export_request(
            self,
            format,
            report,
            chapter,
            start_date=None,
            date_range=None,
            filters=None,
            filter_search_type=None,
            minimum_vuln_info=None,
            plugin_id=None,
            asset_id=None,
    ):
        """Export the given workbench to a file.

        :param format: The file format, one of FORMAT_CSV, FORMAT_HTML, FORMAT_NESSUS, FORMAT_PDF.
        :param report: The type of workbench report, one of REPORT_VULNERABILITIES.
        :param chapter: Chapter to include, one of CHAPTER_EXEC_SUMMARY, CHAPTER_VULN_BY_ASSET, CHAPTER_VULN_BY_PLUGIN,
            CHAPTER_VULN_HOSTS_SUMMARY.
        :param start_date: The date (in unixtime) at which the exported results should begin to be included, default to
            None which implies today.
        :param date_range: The number of days of data prior to and including start_date that should be returned. default
            to None which implies data for all dates is returned.
        :param filters: An list containing filters to apply to the exported scan report, default to None.
        :param filter_search_type: The type of search to be used, one of FILTER_TYPE_AND, FILTER_TYPE_OR, default to
            None.
        :param minimum_vuln_info: When True, only a minimal subset of scan details will be returned for each result,
            excluding plugin attributes. In this case, only plugin_output and vulnerability_state fields are always
            returned; first_found, last_found and last_fixed are also returned if possible. Default to None.
        :param plugin_id: Restrict the export data to only vulnerabilities found by the plugin with this id, default to
            None.
        :param asset_id: Restrict the export data to only findings the asset with this id. Note that this id is a UUID,
            default to None.
        :raise TenableIOApiException:  When API error is encountered.
        :return: The file ID.
        """
        assert format in [WorkbenchesApi.FORMAT_CSV, WorkbenchesApi.FORMAT_HTML, WorkbenchesApi.FORMAT_NESSUS,
                          WorkbenchesApi.FORMAT_PDF, ], u'Valid file format.'
        assert report in [WorkbenchesApi.REPORT_VULNERABILITIES, ], u'Valid report type.'
        assert chapter in [WorkbenchesApi.CHAPTER_EXEC_SUMMARY, WorkbenchesApi.CHAPTER_VULN_BY_ASSET,
                           WorkbenchesApi.CHAPTER_VULN_BY_PLUGIN, WorkbenchesApi.CHAPTER_VULN_HOSTS_SUMMARY,
                           ], u'Valid chapter.'
        assert filter_search_type in [None, WorkbenchesApi.FILTER_TYPE_AND, WorkbenchesApi.FILTER_TYPE_OR,
                                      ], u'Valid filter search type.'

        params = {
            u'format': format,
            u'report': report,
            u'chapter': chapter,
            u'start_date': start_date,
            u'date_range': date_range,
            u'filter': filters,
            u'filter.search_type': filter_search_type,
            u'minimum_vuln_info': minimum_vuln_info,
            u'plugin_id': plugin_id,
            u'asset_id': asset_id,
        }

        response = self._client.get('workbenches/export',
                                    params={k: params[k] for k in params if params[k] is not None})
        return loads(response.text).get('file')

    def export_status(self, file_id):
        """Retrieve the status of a pending export.

        :param file_id: The file ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: The file status.
        """
        response = self._client.get('workbenches/export/%(file_id)s/status',
                                    path_params={'file_id': file_id})
        return loads(response.text).get('status')

    def vulnerabilities(self, age=None, authenticated=None, date_range=None, exploitable=None, filters=None,
                        filter_search_type=None, resolvable=None, severity=None):
        """List all the vulnerabilities recorded.

        :param age: Lists only those vulnerabilities older than a certain number of days.
        :param authenticated: Lists only authenticated vulnerabilities.
        :param date_range: The number of days of data prior to and including today that should be returned.
        :param exploitable: Lists only exploitable vulnerabilities.
        :param filters: An array containing filters to apply to the exported scan report.
        :param filter_search_type: The type of search to be used. Can have a value of **and**(default) or **or**.
        :param resolvable: Lists only those vulnerabilities with a remediation path.
        :param severity: Lists only vulnerabilities of a specific severity (critical, high, medium or low).
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`VulnerabilityList`.
        """
        params = {'age': age, 'authenticated': authenticated, 'date_range': date_range, 'exploitable': exploitable,
                  'filter': filters, 'filter.search_type': filter_search_type, 'resolvable': resolvable,
                  'severity': severity}
        response = self._client.get('workbenches/vulnerabilities',
                                    params={k: v for (k, v) in params.items() if v})
        return VulnerabilityList.from_json(response.text)

    def vulnerability_output(self, plugin_id, date_range=None, filters=None, filter_search_type=None):
        """Get the vulnerability outputs for a plugin.

        :param plugin_id: The plugin id.
        :param date_range: The number of days of data prior to and including today that should be returned.
        :param filters: An array containing filters to apply to the exported scan report.
        :param filter_search_type: The type of search to be used. Can have a value of **and**(default) or **or**.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`VulnerabilityOutputList`.
        """
        params = {'date_range': date_range, 'filter': filters, 'filter.search_type': filter_search_type}
        response = self._client.get('workbenches/vulnerabilities/%(plugin_id)s/outputs',
                                    path_params={'plugin_id': plugin_id},
                                    params={k: v for (k, v) in params.items() if v})
        return VulnerabilityOutputList.from_json(response.text)
