import pytest

from tenable_io.api.users import UserCreateRequest

from tests.base import BaseTest
from tests.config import TenableIOTestConfig


class TestImpersonation(BaseTest):

    @pytest.fixture(scope='class')
    def user(self, app, client):
        user_id = client.users_api.create(UserCreateRequest(
            username=app.session_name(u'test_impersonation%%s@%s' % TenableIOTestConfig.get('users_domain_name')),
            name='test_impersonation',
            password='test_impersonation',
            permissions='16',
            type='local'
        ))
        user = client.users_api.get(user_id)
        yield user
        client.users_api.delete(user_id)

    def test_impersonation(self, client, user):
        impersonating_client = client.impersonate(user.username)
        impersonating_user = impersonating_client.session_api.get()
        assert impersonating_user.username == user.username, u'The current session user should be the impersonated user'
