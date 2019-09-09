import os
import pytest

from tenable_io.api.models import Policy, PolicyDetails, PolicyList, PolicySettings
from tenable_io.api.policies import PolicyConfigureRequest, PolicyImportRequest


@pytest.mark.vcr()
def test_policy_create(new_policy):
    assert isinstance(new_policy, int), u'The `create` method did not return type `int`.'


@pytest.mark.vcr()
def test_policy_details(client, new_policy):
    policy_details = client.policies_api.details(new_policy)
    assert isinstance(policy_details, PolicyDetails), u'The `details` method did not return type `PolicyDetails`.'


@pytest.mark.vcr()
def test_policy_list(client):
    policy_list = client.policies_api.list()
    assert isinstance(policy_list, PolicyList), u'The `list` method did not return type `PolicyList`.'
    for policy in policy_list.policies:
        assert isinstance(policy, Policy), u'Should be a list of type `Policy`.'


@pytest.mark.vcr()
def test_policy_delete(client, new_policy):
    assert client.policies_api.delete(new_policy), u'The policy was not deleted.'


@pytest.mark.vcr()
def test_policy_configure(client, new_policy):
    policy_id = new_policy
    policy_configure_request = PolicyConfigureRequest(
        policy_id,
        PolicySettings(
                name='policy_name_edit'
            )
    )
    assert client.policies_api.configure(policy_id, policy_configure_request), u'The policy was not edited.'

    edited_policy = client.policies_api.details(policy_id)
    assert edited_policy.settings.name == 'policy_name_edit', \
        u'The returned policy name should match the the edited value.'


@pytest.mark.vcr()
def test_policy_copy(client, new_policy):
    policy_id = new_policy
    copy_of_policy_id = client.policies_api.copy(policy_id)
    assert isinstance(copy_of_policy_id, int), u'The `copy` method did not return type `int`.'
    policy_details = client.policies_api.details(policy_id)
    copy_policy_details = client.policies_api.details(copy_of_policy_id)
    assert policy_details.settings.description == copy_policy_details.settings.description, \
        u'Expected the copy of the policy to have the same description as the original.'


@pytest.mark.vcr()
def test_policy_import_and_export(client, new_policy):
    policy_id = new_policy
    iter_content = client.policies_api.export(policy_id, False)

    path = 'test_policies_export_and_import'
    with open(path, 'wb') as fd:
        for chunk in iter_content:
            fd.write(chunk)
    assert os.path.isfile(path), u'The policy file has been downloaded'
    assert os.path.getsize(path) > 0, u'The policy file is not empty.'

    with open(path, 'rb') as fu:
        upload_file_name = client.file_api.upload(fu)
    assert upload_file_name, u'File `upload` method returns valid file name.'

    imported_policy_id = client.policies_api.import_policy(PolicyImportRequest(upload_file_name))
    assert isinstance(imported_policy_id, int), u'The import request returns policy id.'

    policy = client.policies_api.details(policy_id)
    imported_policy = client.policies_api.details(imported_policy_id)
    assert policy.settings.description == imported_policy.settings.description, \
        u'The description` field is the same'

    response = client.policies_api.delete(imported_policy_id)
    assert response is True, u'The `delete` method returns True.'
    os.remove(path)
