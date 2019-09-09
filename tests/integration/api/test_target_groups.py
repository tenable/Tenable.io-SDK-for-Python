import pytest

from tenable_io.api.target_groups import TargetListEditRequest
from tenable_io.api.models import TargetGroup, TargetGroupList


@pytest.mark.vcr()
def test_target_groups_create(new_target_group):
    assert isinstance(new_target_group, TargetGroup), u'The `create` method did not return type `TargetGroup`.'


@pytest.mark.vcr()
def test_target_groups_details(client, new_target_group):
    target_group = new_target_group
    details = client.target_groups_api.details(target_group.id)
    assert isinstance(details, TargetGroup), u'The `details` method did not return type `TargetGroup`.'
    assert details.id == target_group.id, u'Expected the `details` response to match the requested target group.'


@pytest.mark.vcr()
def test_target_groups_list(client):
    target_groups = client.target_groups_api.list()
    assert isinstance(target_groups, TargetGroupList), u'The `details` method did not return type `TargetGroup`.'
    for group in target_groups.target_groups:
        assert isinstance(group, TargetGroup), u'Expected a list of type `TargetGroup`.'


@pytest.mark.vcr()
def test_target_groups_delete(client, new_target_group):
    assert client.target_groups_api.delete(new_target_group.id), u'The target group was not deleted.'


@pytest.mark.vcr()
def test_target_groups_edit(client, new_target_group):
    target_group = new_target_group
    edited_name = 'test_target_group_edit'
    edited_group = client.target_groups_api.edit(TargetListEditRequest(name=edited_name), target_group.id)
    assert isinstance(edited_group, TargetGroup), u'The `edit` method did not return type `TargetGroup`.'
    assert edited_group.id == target_group.id, u'Expected the edited target group to match the requested target group.'
    assert edited_group.name == edited_name, u'Expected the name to be updated.'
