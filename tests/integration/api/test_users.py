import pytest

from random import randint
from tenable_io.api.models import Permissions, User, UserKeys, UserList
from tenable_io.api.users import UserCreateRequest, UserEditRequest

from tests.config import TenableIOTestConfig


def create_user(client, role):
    return client.users_api.create(UserCreateRequest(
        username='test_user_{}_{}@{}'.format(role, randint(0, 10000), TenableIOTestConfig.get('users_domain_name')),
        name='test_users',
        password='Sdk!Test1',
        permissions="{}".format(get_permission(role)),
        type='local',
        email='test_user_{}_{}@{}'.format(role, randint(0, 10000), TenableIOTestConfig.get('users_domain_name'))
    ))


def get_permission(role):
    if role == 'admin':
        return Permissions.User.PERMISSION_ADMINISTRATOR
    elif role == 'scan_manager':
        return Permissions.User.PERMISSION_SCAN_MANAGER
    elif role == 'standard':
        return Permissions.User.PERMISSION_STANDARD
    elif role == 'scan_operator':
        return Permissions.User.PERMISSION_SCAN_OPERATOR
    else:
        return Permissions.User.PERMISSION_BASIC


@pytest.mark.vcr()
def test_users_create(client):
    user_id = create_user(client, 'admin')
    assert isinstance(user_id, int), u'The `create` method did not return type `int`.'


@pytest.mark.vcr()
def test_users_list(client):
    users = client.users_api.list()
    assert isinstance(users, UserList), u'The `list` method did not return type `UserList`.'
    for user in users.users:
        assert isinstance(user, User), u'Expected a list of type `User`.'


@pytest.mark.vcr()
def test_users_get(client):
    user_id = create_user(client, 'scan_operator')
    user_from_get = client.users_api.get(user_id)
    assert isinstance(user_from_get, User), u'The `get` method did not return type `User`.'
    assert user_from_get.id == user_id, u'Expected the `get` response to match the requested user.'

    user_from_details = client.users_api.details(user_id)
    assert isinstance(user_from_details, User), u'The `details` method did not return type `User`.'
    assert user_from_details.id == user_id, u'Expected the `details` response to match the requested user.'


@pytest.mark.vcr()
def test_users_edit(client):
    user_id = create_user(client, 'scan_manager')
    edited_name = 'test_user_edited'
    edit_request = UserEditRequest(
        name=edited_name
    )
    edited_user = client.users_api.edit(user_id, edit_request)
    assert isinstance(edited_user, User), u'The `edit` method did not return type `User`.'
    assert edited_user.id == user_id, u'Expected the `edit` response to match the requested user.'
    assert edited_user.name == edited_name, u'Expected the name to be updated.'


@pytest.mark.vcr()
def test_users_edit_password(client):
    user_id = create_user(client, 'basic')
    new_password = 'Sdk!Test2'
    assert client.users_api.password(user_id, new_password), u'A new password should be set.'


@pytest.mark.vcr()
def test_users_delete(client):
    user_id = create_user(client, 'standard')
    assert client.users_api.delete(user_id), u'The user was not deleted.'


@pytest.mark.vcr()
def test_users_keys(client):
    user_id = create_user(client, 'standard')
    keys = client.users_api.keys(user_id)
    assert isinstance(keys, UserKeys), u'The `keys` method did not return type `UserKeys`.'


@pytest.mark.vcr()
def test_users_enabled(client):
    user_id = create_user(client, 'standard')
    assert client.users_api.enabled(user_id, False), u'The user was not disabled.'
