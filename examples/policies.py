import os

from tenable_io.client import TenableIOClient
from tenable_io.exceptions import TenableIOApiException


def example(test_name, test_file):

    # Generate unique file.
    policy_name = test_name(u'my test policy')
    test_file_output = test_file(u'my_exported_policy.tenable_io')

    '''
    Instantiate an instance of the TenableIOClient.
    '''
    client = TenableIOClient()

    '''
    Create a policy.
    '''
    policy = client.policy_helper.create(
        name=policy_name,
        template='discovery'
    )
    assert policy.name() == policy_name

    '''
    Export a policy into a NESSUS file.
    '''
    policy.download(test_file_output)
    assert os.path.isfile(test_file_output)

    '''
    Import a policy from a NESSUS file and get the detail.
    '''
    imported_policy = client.policy_helper.import_policy(test_file_output)
    assert imported_policy.details().uuid == policy.details().uuid
    os.remove(test_file_output)

    '''
    Create a new policy by copying a policy.
    '''
    policy_copy = policy.copy()
    assert policy_copy.id != policy.id

    '''
    Delete policies.
    '''
    policy.delete()
    imported_policy.delete()
    policy_copy.delete()
    try:
        policy.details()
        assert False
    except TenableIOApiException:
        pass
    try:
        imported_policy.details()
        assert False
    except TenableIOApiException:
        pass
    try:
        policy_copy.details()
        assert False
    except TenableIOApiException:
        pass
