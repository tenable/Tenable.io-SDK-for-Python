import os
import pytest

from tests.config import TenableIOTestConfig


def create_policy(client):
    return client.policy_helper.create(
        'test_policy',
        TenableIOTestConfig.get('policy_template_name')
    )


@pytest.mark.vcr()
def test_policy_helper_details(client):
    policy = create_policy(client)
    policy_details = policy.details()
    assert policy_details.settings.name == policy.name(), u'PolicyRef `name` should match the name in PolicyDetail.'


@pytest.mark.vcr()
def test_policy_helper_download_import(client):
    policy = create_policy(client)
    download_path = 'test_policy_download'

    assert not os.path.isfile(download_path), u'Policy file does not exist yet.'

    policy.download(download_path)

    assert os.path.isfile(download_path), u'Policy file is downloaded.'

    imported_policy = client.policy_helper.import_policy(download_path)

    # Server will add suffix if importing a policy file with duplicate name.
    imported_policy_name = imported_policy.name()
    assert policy.name() in imported_policy_name, \
        u'Imported policy file has the same name as the downloaded policy.'

    imported_policy.delete()

    os.remove(download_path)
    assert not os.path.isfile(download_path), u'Policy file is deleted.'
