import pytest

from tenable_io.api.models import Plugin, PluginAttribute, PluginDetails, PluginFamily, PluginFamilyDetails, \
    PluginFamilyList


@pytest.mark.vcr()
def test_plugins_families(client):
    family_list = client.plugins_api.families()
    assert isinstance(family_list, PluginFamilyList), u'The `families` method did not return type `PluginFamilyList`.'
    assert len(family_list.families) > 0, u'Service expect return at least 1 plugin family.'
    for f in family_list.families:
        assert isinstance(f, PluginFamily), u'families should have type of `PluginFamily`.'


@pytest.mark.vcr()
def test_plugins_family_details(client):
    family_list = client.plugins_api.families()
    family_details = client.plugins_api.family_details(family_list.families[0].id)
    assert isinstance(family_details, PluginFamilyDetails), \
        u'The `family_details` method did not return type `PluginFamilyDetails`.'
    for p in family_details.plugins:
        isinstance(p, Plugin), u'List has instances of type.'


@pytest.mark.vcr()
def test_plugins_plugin_details(client):
    family_list = client.plugins_api.families()
    family_details = client.plugins_api.family_details(family_list.families[0].id)
    assert len(family_details.plugins) > 0, u'Plugin family should contain plugins.'
    plugin_details = client.plugins_api.plugin_details(family_details.plugins[0].id)
    assert isinstance(plugin_details,
                      PluginDetails), u'The `plugin_details` method did not return type `PluginDetails`.'
    for a in plugin_details.attributes:
        isinstance(a, PluginAttribute), u'List has instances of type.'
