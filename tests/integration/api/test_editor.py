import pytest

from tenable_io.api.editor import SCAN, POLICY
from tenable_io.api.models import EditorConfigurationDetails, EditorPluginAttributes, EditorPluginDescription, \
    EditorTemplateDetails, TemplateList, PolicySettings
from tenable_io.api.policies import PolicyCreateRequest


@pytest.mark.vcr()
def test_editor_list(client):
    template_list = client.editor_api.list(SCAN)
    assert isinstance(template_list, TemplateList), u'The `list` method did not return type `TemplateList`.'
    policy_list = client.editor_api.list(POLICY)
    assert isinstance(policy_list, TemplateList), u'The `list` method did not return type `TemplateList`.'


@pytest.mark.vcr()
def test_editor_details(client, new_scan_id):
    scan_configuration_details = client.editor_api.details(SCAN, new_scan_id)
    assert isinstance(scan_configuration_details, EditorConfigurationDetails), \
        u'The `details` method did not return type `EditorConfigurationDetails`.'


@pytest.mark.vcr()
def test_editor_template_details(client):
    template_list = client.editor_api.list(SCAN)
    scan_template_details = client.editor_api.template_details(SCAN, template_list.templates[0].uuid)
    assert isinstance(scan_template_details, EditorTemplateDetails), \
        u'The `template_details` method did not return type `EditorTemplateDetails`.'


@pytest.mark.vcr()
def test_editor_plugin_details(client):
    # create new policy based on advanced template
    template_list = client.editor_api.list(POLICY)
    aadvanced_template = [t for t in template_list.templates if t.name == 'advanced']
    policy_id = client.policies_api.create(
        PolicyCreateRequest(
            aadvanced_template[0].uuid,
            PolicySettings(
                name='test_policy_advanced',
                description='test_policies'
            )
        )
    )

    plugin_details = client.editor_api.plugin_details(policy_id=policy_id, family_id=22, plugin_id=72663)
    assert isinstance(plugin_details, EditorPluginDescription), \
        u'The `plugin_details` method did not return type `EditorPluginDescription`.'
    assert isinstance(plugin_details.pluginattributes, EditorPluginAttributes), \
        u'The `pluginattributes` method did not return type `EditorPluginAttributes`.'
