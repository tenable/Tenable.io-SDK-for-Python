import random

from tenable_io.client import TenableIOClient
from tenable_io.exceptions import TenableIOApiException
from tenable_io.api.models import User, Permissions
from tenable_io.api.users import UserCreateRequest, UserEditRequest


def example(test_domain):

    test_user_name = u'example_test_user_{}'.format(random.randint(1, 100))
    test_user_username = u'{}@{}'.format(test_user_name, test_domain)

    '''
    Instantiate an instance of the TenableIOClient.
    '''
    client = TenableIOClient()

    '''
    Create a new Standard User
    '''
    user_create_request = UserCreateRequest(username=test_user_username,
                                            password='Sdk!Test1234{}'.format(random.randint(1, 100)),
                                            permissions=Permissions.User.PERMISSION_STANDARD,
                                            name=test_user_name,
                                            email=test_user_username,
                                            type=User.LOCAL)
    std_user_id = client.users_api.create(user_create_request)
    assert std_user_id

    '''
    Fetch user details
    '''
    std_user = client.users_api.details(std_user_id)
    assert isinstance(std_user, User)
    assert std_user.permissions == Permissions.User.PERMISSION_STANDARD


    '''
    Check that new user is included in user list
    '''
    user_list = client.users_api.list()
    assert any([u.id for u in user_list.users if u.id == std_user_id])

    '''
    Edit user
    '''
    user_edit_request = UserEditRequest(permissions=Permissions.User.PERMISSION_SCAN_MANAGER)
    edited_std_user = client.users_api.edit(std_user_id, user_edit_request)
    assert isinstance(edited_std_user, User)
    assert edited_std_user.permissions == Permissions.User.PERMISSION_SCAN_MANAGER

    '''
    Delete user
    '''
    assert client.users_api.delete(std_user_id)

    '''
    Check that deleted user is not included in user list
    '''
    user_list = client.users_api.list()
    assert not any([u.id for u in user_list.users if u.id == std_user_id])
