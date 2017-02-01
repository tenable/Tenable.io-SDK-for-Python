import os
import pytest

from tests.base import BaseTest
from tests.config import TenableIOTestConfig


class TestPolicyHelper(BaseTest):

    @pytest.fixture(scope='class')
    def policy(self, app, client):
        """
        Creata a policy for testing.
        """
        policy = client.policy_helper.create(
            app.session_name('test_policy'),
            TenableIOTestConfig.get('policy_template_name'))
        yield policy
        policy.delete()

    def test_details(self, policy):
        policy_details = policy.details()
        assert policy_details.settings.name == policy.name(), u'PolicyRef `name` should match the name in PolicyDetail.'

    def test_download_import(self, app, client, policy):
        download_path = app.session_file_output('test_policy_download')

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
