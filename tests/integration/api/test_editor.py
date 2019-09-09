import pytest

from tenable_io.api.models import TemplateList


@pytest.mark.vcr()
def test_editor_list(client):
    template_list = client.editor_api.list('scan')
    assert isinstance(template_list, TemplateList), u'The `list` method did not return type `TemplateList`.'
    policy_list = client.editor_api.list('policy')
    assert isinstance(policy_list, TemplateList), u'The `list` method did not return type `TemplateList`.'
