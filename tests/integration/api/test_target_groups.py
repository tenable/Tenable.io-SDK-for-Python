import pytest

from tenable_io.api.target_groups import TargetGroupCreateRequest
from tenable_io.api.models import TargetGroup, TargetGroupList
from tests.base import BaseTest


class TestTargetGroupsApi(BaseTest):

    @pytest.fixture(scope='class')
    def target_group(self, app, client):
        target_group = client.target_groups_api.create(TargetGroupCreateRequest(
            name=app.session_name('test_target_groups'),
            members='tenable.com',
            type='system',
            acls=[{"permissions": 0, "type": "default"}]
        ))
        yield target_group
        assert client.target_groups_api.delete(target_group.id), u'Target group is deleted.'

    def test_list_return_correct_type(self, client):
        target_group_list = client.target_groups_api.list()
        assert isinstance(target_group_list, TargetGroupList), u'The `list` method return type.'

    def test_create_delete(self, app, client):
        target_group = client.target_groups_api.create(TargetGroupCreateRequest(
            name=app.session_name('test_create_delete'),
            members='tenable.com',
            type='system',
            acls=[{"permissions": 0, "type": "default"}]
        ))
        assert isinstance(target_group, TargetGroup), u'The `create` method return type.'
        assert hasattr(target_group, 'id'), u'Target group has ID.'
        assert hasattr(target_group, 'acls') and target_group.acls, u'Target group has nonempty acls.'
        assert client.target_groups_api.delete(target_group.id), u'Target group is deleted.'

    def test_get(self, target_group, client):
        got_target_group = client.target_groups_api.details(target_group.id)
        assert got_target_group.id == target_group.id, u'The `details` method returns target group with matching ID.'

    def test_edit(self, app, client, target_group):
        previous_name = target_group.name
        new_name = app.session_name('test_edit')

        edited_target_group = client.target_groups_api.edit(TargetGroupCreateRequest(
            name=new_name,
            members=target_group.members,
            type=target_group.type,
        ), target_group.id)
        assert edited_target_group.name == new_name, u'The `edit` method returns target group with matching name.'

        got_target_group = client.target_groups_api.details(edited_target_group.id)
        assert got_target_group.name == new_name, u'The `details` method returns target group with matching name.'

        reverted_target_group = client.target_groups_api.edit(TargetGroupCreateRequest(
            name=previous_name,
            members=got_target_group.members,
            type=got_target_group.type,
        ), target_group.id)
        assert reverted_target_group.name == previous_name, u'The reverted target group has matching name.'

    def test_list(self, client, target_group):
        target_group_list = client.target_groups_api.list()
        for l in target_group_list.target_groups:
            assert isinstance(l, TargetGroup), u'Target group list\'s element type.'
        assert len([l for l in target_group_list.target_groups if l.id == target_group.id]) == 1, \
            u'Target group list contains created target group.'
