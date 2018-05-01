import pytest
import random

from tests.base import BaseTest
from tenable_io.api.models import Permissions


class TestPermissionsHelper(BaseTest):

    def test_default_scan(self, client):
        default_view = client.permissions_helper.default_scan(Permissions.Scan.PERMISSION_CAN_VIEW)
        assert isinstance(default_view, Permissions)
        assert default_view.type == u'default'
        assert default_view.permissions == 16

        default_control = client.permissions_helper.default_scan(Permissions.Scan.PERMISSION_CAN_CONTROL)
        assert isinstance(default_control, Permissions)
        assert default_control.type == u'default'
        assert default_control.permissions == 32

    def test_user_scan(self, client):
        test_user = random.choice(client.users_api.list().users)
        user_control = client.permissions_helper.user_scan(test_user.id, Permissions.Scan.PERMISSION_CAN_CONTROL)
        assert isinstance(user_control, Permissions)
        assert user_control.type == u'user'
        assert user_control.permissions == 32
        assert user_control.name == test_user.name
