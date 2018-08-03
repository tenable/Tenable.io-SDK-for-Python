from tenable_io.api.base import BaseApi
from tenable_io.api.models import PluginDetails, PluginFamilyDetails, PluginFamilyList


class PluginsApi(BaseApi):

    def families(self, include_all=None):
        """Return list of plugin families.

        :param include_all: Whether or not to include all plugins. Defaults to be less inclusive.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.PluginFamilyList`.
        """
        params = {'all': include_all}
        response = self._client.get('plugins/families', params={k: v for (k, v) in params.items() if v})
        return PluginFamilyList.from_json(response.text)

    def family_details(self, family_id):
        """Return plugin family details.

        :param family_id: Plugin family ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.PluginFamilyDetails`.
        """
        response = self._client.get('plugins/families/%(id)s', path_params={'id': family_id})
        return PluginFamilyDetails.from_json(response.text)

    def plugin_details(self, plugin_id):
        """Return plugin details.

        :param plugin_id: Plugin ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.PluginDetails`.
        """
        response = self._client.get('plugins/plugin/%(id)s', path_params={'id': plugin_id})
        return PluginDetails.from_json(response.text)
