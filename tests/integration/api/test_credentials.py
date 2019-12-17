import pytest

from random import randint
from tenable_io.api.credentials import CredentialRequest
from tenable_io.api.models import CredentialDetails, CredentialList, CredentialPermission, CredentialPrimitiveType


@pytest.mark.vcr()
def test_managed_credential_details(client):
    new_credential_uuid = create_managed_credential(client)
    resp = client.credentials_api.details(uuid=new_credential_uuid)
    assert isinstance(resp, CredentialDetails), u'The `details` method did not return type `CredentialDetails`.'
    assert resp.type.name == 'Windows', u'Expected the returned type to match the configured type.'


@pytest.mark.vcr()
def test_managed_credential_list(client):
    resp = client.credentials_api.list()
    assert isinstance(resp, CredentialList), u'The `list` method did not return type `CredentialList`.'


@pytest.mark.vcr()
def test_managed_credential_delete(client):
    new_credential_uuid = create_managed_credential(client)
    assert client.credentials_api.delete(new_credential_uuid), u'The `delete` method did not return successfully.'


@pytest.mark.vcr()
def test_managed_credential_update(client):
    new_credential_uuid = create_managed_credential(client)
    edited_name = 'Edited Credential Name'
    req = CredentialRequest(name=edited_name)
    assert client.credentials_api.update(new_credential_uuid, req), u'The `update` method did not return successfully.'
    resp = client.credentials_api.details(uuid=new_credential_uuid)
    assert resp.name == edited_name, u'Expected the credential name to have been updated'


@pytest.mark.vcr()
def test_managed_credential_types(client):
    resp = client.credentials_api.types()
    assert isinstance(resp, CredentialPrimitiveType), \
        u'The `types` method did not return type `CredentialPrimitiveType`.'


def create_managed_credential(client):
    test_user = client.users_api.list().users[0]
    permission = CredentialPermission(grantee_uuid=test_user.uuid,
                                      type=CredentialPermission.USER_TYPE,
                                      permissions=CredentialPermission.CAN_USE,
                                      name=test_user.username,
                                      isPending=True)
    req = CredentialRequest(name='test_credential_name{}'.format(randint(0, 100)),
                            description='test credential',
                            type_='Windows',
                            settings={
                                "domain": "",
                                "username": "user@example.com",
                                "auth_method": "Password",
                                "password": "aJ^deq34Rc"
                            }, permissions=[permission])
    return client.credentials_api.create(req)
