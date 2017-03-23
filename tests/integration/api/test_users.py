import pytest

from tenable_io.api.models import User, UserList
from tenable_io.api.users import UserCreateRequest
from tenable_io.api.users import UserEditRequest

from tests.base import BaseTest
from tests.config import TenableIOTestConfig


class TestUsersApi(BaseTest):

    @pytest.fixture(scope='class')
    def user_id(self, app, client):
        new_user = client.users_api.create(UserCreateRequest(
            username=app.session_name(u'test_users+%%s@%s' % TenableIOTestConfig.get('users_domain_name')),
            name='test_users',
            password='test_users',
            permissions="16",
            type='local',
            email=app.session_name(u'test_user_email+%%s@%s' % TenableIOTestConfig.get('users_domain_name'))
        ))
        yield new_user
        client.users_api.delete(new_user)

    def test_list_return_correct_type(self, client):
        user_list = client.users_api.list()
        assert isinstance(user_list, UserList), u'The `list` method returns type.'

    def test_get_return_correct_user(self, client):
        user_list = client.users_api.list()

        assert len(user_list.users) > 0, u'User list has at least one user for testing.'

        user = user_list.users[0]

        assert hasattr(user, 'id'), u'User has ID.'

        got_user = client.users_api.get(user.id)

        assert got_user.id == user.id, u'The `get` method returns user with the same ID.'
        assert got_user.email == user.email, u'The `get` method returns user with the same email.'
        assert got_user.username == user.username, u'The `get` method returns user with the same username.'

    def test_users_create(self, app, client):
        new_user_id = client.users_api.create(UserCreateRequest(
            username=app.session_name(u'test_users_create+%%s@%s' % TenableIOTestConfig.get('users_domain_name')),
            name='test_users_create',
            password='test_users_create',
            permissions='16',
            type='local',
            email=app.session_name(u'test_user_email+%%s@%s' % TenableIOTestConfig.get('users_domain_name'))
        ))

        assert type(new_user_id) == int, u'User responded with ID of integer type.'
        client.users_api.delete(new_user_id)

    def test_users_edit(self, user_id, app, client):
        user_info = client.users_api.get(user_id)
        previous_name = user_info.name
        new_name = 'test_users_edit'

        edited_user = client.users_api.edit(user_id, UserEditRequest(
            name=new_name,
            email=app.session_name(u'test_user_email+%%s@%s' % TenableIOTestConfig.get('users_domain_name'))
        ))
        assert edited_user.name == new_name, u'The `edit` method returns user with matching name.'

        reverted_edit_user = client.users_api.edit(user_id, UserEditRequest(
            name=previous_name,
            email=app.session_name(u'test_user_email+%%s@%s' % TenableIOTestConfig.get('users_domain_name'))
        ))
        assert reverted_edit_user.name == previous_name, u'The reverted user has matching name.'

    def test_list(self, user_id, client):
        user_list = client.users_api.list()
        for user in user_list.users:
            assert isinstance(user, User), u'User list\'s element type.'
        assert len([user for user in user_list.users if user.id == user_id]) == 1, u'User list contains created user.'

    def test_edit_password(self, client):
        new_password = 'test_edit_password'

        assert client.users_api.password(8, new_password), u'A new password should be set.'

    def test_get_details(self, client):
        user_list = client.users_api.list()
        assert len(user_list.users) > 0, u'User list has at least one user for testing.'

        user = user_list.users[0]

        detail_list = client.users_api.details(user.id)
        assert detail_list.id == user.id, u'The user ID returned should match the requested ID.'

    def test_keys(self, client, user_id):
        user_keys_a = client.users_api.keys(user_id)
        user_keys_b = client.users_api.keys(user_id)

        assert user_keys_a.access_key != user_keys_b.access_key, u'Generated access key should change every time.'
        assert user_keys_a.secret_key != user_keys_b.secret_key, u'Generated secret key should change every time.'

    def test_enabled(self, client, user_id):
        client.users_api.enabled(user_id, False)

        check_disabled_user = client.users_api.details(user_id)
        assert not check_disabled_user.enabled, u'The user should be disabled.'

        client.users_api.enabled(user_id, True)

        check_enabled_user = client.users_api.details(user_id)
        assert check_enabled_user.enabled, u'The user should be set back to enabled.'
