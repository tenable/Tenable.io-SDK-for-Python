import pytest

from tests.base import BaseTest
from tenable_io.api.models import Group


class TestGroupsApi(BaseTest):

    @pytest.fixture(scope='class')
    def group(self, app, client):
        name = app.session_name('test_group')
        group = client.groups_api.create(name)
        yield group
        assert client.groups_api.delete(group.id), u'The group should be deleted.'

    def test_create_delete(self, app, client):
        name = app.session_name('test_create_delete')
        group = client.groups_api.create(name)

        assert isinstance(group, Group), u'The create method returns type.'
        assert hasattr(group, 'id'), u'The group has ID.'

        client.groups_api.delete(group.id)
        assert self._get_group_from_group_list(client, group.id) is None, u'The group is deleted.'

    def test_list_group(self, client, group):
        group_list = client.groups_api.list()

        for g in group_list.groups:
            assert isinstance(g, Group), u'Group list\'s element type.'

        assert len([g for g in group_list.groups if g.id == group.id]) == 1, \
            u'Group list contains the created group.'

    def test_edit(self, app, client, group):
        previous_name = group.name
        new_name = app.session_name('test_edit')

        assert client.groups_api.edit(group.id, new_name), u'The group name has been edited.'
        edited_group = self._get_group_from_group_list(client, group.id)
        assert edited_group, u'The edited group exists.'
        assert edited_group.name == new_name, u'The edited group returned from group list matches the edited name.'

        client.groups_api.edit(group.id, previous_name)
        reverted_group = self._get_group_from_group_list(client, group.id)
        assert reverted_group, u'The reverted group exists.'
        assert reverted_group.name == previous_name, \
            u'The reverted group returned from group list matches the reverted name.'

    def test_add_delete_list_group_users(self, client, group):
        user_list = client.users_api.list()

        assert len(user_list.users) > 0, u'User list has at least one user for testing.'
        user = user_list.users[0]

        assert hasattr(user, 'id'), u'User has ID.'
        client.groups_api.add_user(group.id, user.id)

        user_list = client.groups_api.list_users(group.id)
        assert len([u for u in user_list.users if u.id == user.id]) > 0, \
            u'The user returned from group list matches user added to the group.'

        client.groups_api.delete_user(group.id, user.id)

        new_user_list = client.groups_api.list_users(group.id)
        assert len([u for u in new_user_list.users if u.id == user.id]) == 0, \
            u'The removed user is not shown in the group list.'

    @staticmethod
    def _get_group_from_group_list(client, id):
        group_list = client.groups_api.list()
        matching_groups = [f for f in group_list.groups if f.id == id]
        return matching_groups[0] if len(matching_groups) > 0 else None
