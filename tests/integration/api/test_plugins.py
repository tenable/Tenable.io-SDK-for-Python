from tenable_io.api.models import Plugin, PluginAttribute, PluginDetails, PluginFamily, PluginFamilyDetails, \
    PluginFamilyList

from tests.base import BaseTest


class TestPluginsApi(BaseTest):

    def test_plugin_families_family_details_plugin_details(self, client):
        family_list = client.plugins_api.families()
        assert isinstance(family_list, PluginFamilyList), u'The method returns plugin family list.'
        assert len(family_list.families) > 0, u'Service expect return at least 1 plugin family.'

        for f in family_list.families:
            assert isinstance(f, PluginFamily), u'List has instances of type.'

        family_id = family_list.families[0].id
        assert isinstance(family_id, int), u'ID is `int` type.'

        family_details = client.plugins_api.family_details(family_id)
        assert isinstance(family_details, PluginFamilyDetails)
        assert len(family_details.plugins) > 0, u'Service expect to return at least 1 plugin.'

        for p in family_details.plugins:
            isinstance(p, Plugin), u'List has instances of type.'

        plugin_id = family_details.plugins[0].id
        assert isinstance(plugin_id, int), u'ID is `int` type.'

        plugin_details = client.plugins_api.plugin_details(plugin_id)
        assert isinstance(plugin_details, PluginDetails)

        for a in plugin_details.attributes:
            isinstance(a, PluginAttribute), u'List has instances of type.'
