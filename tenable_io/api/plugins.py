from tenable_io.api.base import BaseApi
from tenable_io.api.models import PluginDetails, PluginFamilyDetails, PluginFamilyList


class PluginsApi(BaseApi):

    def families(self):
        """Return list of plugin families.

        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.PluginFamilyList`.
        """
        response = self._client.get('plugins/families')
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
