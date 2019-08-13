import pytest

from tenable_io.api.models import Permissions


@pytest.mark.vcr()
def test_permissions_helper_default_scan(client):
    default_view = client.permissions_helper.default_scan(Permissions.Scan.PERMISSION_CAN_VIEW)
    assert isinstance(default_view, Permissions)
    assert default_view.type == u'default'
    assert default_view.permissions == 16

    default_control = client.permissions_helper.default_scan(Permissions.Scan.PERMISSION_CAN_CONTROL)
    assert isinstance(default_control, Permissions)
    assert default_control.type == u'default'
    assert default_control.permissions == 32

@pytest.mark.vcr()
def test_permissions_helper_user_scan(client):
    test_user = client.users_api.list().users[0]
    user_control = client.permissions_helper.user_scan(test_user.id, Permissions.Scan.PERMISSION_CAN_CONTROL)
    assert isinstance(user_control, Permissions)
    assert user_control.type == u'user'
    assert user_control.permissions == 32
    assert user_control.name == test_user.name
