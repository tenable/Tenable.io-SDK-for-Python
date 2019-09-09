import pytest

from tenable_io.api.models import Group, GroupList


@pytest.mark.vcr()
def test_groups_create(new_group):
    assert isinstance(new_group, Group), u'The `create` method did not return type `Group`.'


@pytest.mark.vcr()
def test_groups_list(client):
    group_list = client.groups_api.list()
    assert isinstance(group_list, GroupList), u'The `list` method did not return type `GroupList`.'


@pytest.mark.vcr()
def test_groups_edit(client, new_group):
    group = new_group
    assert client.groups_api.edit(group.id, 'test_group_edited'), u'The group name was not edited.'
    group_list = client.groups_api.list()
    edited_group = [g for g in group_list.groups if g.id == group.id]
    assert edited_group[0].name == 'test_group_edited', u'The returned group name should match the the edited value.'


@pytest.mark.vcr()
def test_group_users(client, new_group):
    # test will add, list, and remove users from a group
    group = new_group
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
