from json import loads

from tenable_io.api.base import BaseApi
from tenable_io.api.models import AssetList, AssetInfo, VulnerabilityList, \
    VulnerabilityOutputList


class WorkbenchApi(BaseApi):

    def assets(self, date_range=None, filters=None, filter_search_type=None):
        """List all the assets recorded.

        :param date_range: The number of days of data prior to and including today that should be returned.
        :param filters: An array containing filters to apply to the exported scan report.
        :param filter_search_type: The type of search to be used. Can have a value of **and**(default) or **or**.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`AssetList`.
        """
        params = {'date_range': date_range, 'filters': filters, 'filter_search_type': filter_search_type}
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
        params = {'date_range': date_range, 'filters': filters, 'filter_search_type': filter_search_type}
        response = self._client.get('workbenches/assets/vulnerabilities',
                                    params={k: v for (k, v) in params.items() if v})
        return AssetList.from_json(response.text)

    def asset_info(self, asset_id, date_range=None, filters=None, filter_search_type=None):
        """List detailed info of an asset.

        :param asset_id: The asset ID.
        :param date_range: The number of days of data prior to and including today that should be returned.
        :param filters: An array containing filters to apply to the exported scan report.
        :param filter_search_type: The type of search to be used. Can have a value of **and**(default) or **or**.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`AssetInfo`.
        """
        params = {'date_range': date_range, 'filters': filters, 'filter_search_type': filter_search_type}
        response = self._client.get('workbenches/assets/%(asset_id)s/info',
                                    params={k: v for (k, v) in params.items() if v},
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
        params = {'date_range': date_range, 'filters': filters, 'filter_search_type': filter_search_type}
        response = self._client.get('workbenches/assets/%(asset_id)s/vulnerabilities',
                                    params={k: v for (k, v) in params.items() if v},
                                    path_params={'asset_id': asset_id})
        return VulnerabilityList.from_json(response.text)

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
                  'filters=': filters, 'filter_search_type': filter_search_type, 'resolvable': resolvable,
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
        params = {'date_range': date_range, 'filters': filters, 'filter_search_type': filter_search_type}
        response = self._client.get('workbenches/vulnerabilities/%(plugin_id)s/outputs',
                                    path_params={'plugin_id': plugin_id},
                                    params={k: v for (k, v) in params.items() if v})
        return VulnerabilityOutputList.from_json(response.text)
