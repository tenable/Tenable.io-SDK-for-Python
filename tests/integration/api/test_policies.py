import pytest
import os

from tenable_io.api.models import Policy, PolicyDetails, PolicyList, PolicySettings
from tenable_io.api.policies import PolicyCreateRequest, PolicyConfigureRequest, PolicyImportRequest

from tests.base import BaseTest
from tests.config import TenableIOTestConfig


class TestPoliciesApi(BaseTest):

    @pytest.fixture(scope='class')
    def template(self, client):
        """
        Get policy template for testing.
        """
        template_list = client.editor_api.list('policy')
        assert len(template_list.templates) > 0, u'At least one policy template.'

        test_templates = [t for t in template_list.templates
                          if t.name == TenableIOTestConfig.get('policy_template_name')]
        assert len(test_templates) > 0, u'At least one test template.'

        yield test_templates[0]

    @pytest.fixture(scope='class')
    def policy_id(self, app, client, template):
        """
        Create a policy for testing.
        """
        policy_id = client.policies_api.create(
            PolicyCreateRequest(
                template.uuid,
                PolicySettings(
                    name=app.session_name('test_policies'),
                    description='test_policies'
                )
            )
        )
        assert isinstance(policy_id, int), u'The `create` method returns a policy id.'
        yield policy_id

        response = client.policies_api.delete(policy_id)
        assert response is True, u'The `delete` method returns True.'

    def test_details(self, client, policy_id):
        policy = client.policies_api.details(policy_id)
        assert isinstance(policy, PolicyDetails), u'The `details` method returns type.'
        assert isinstance(policy.settings, PolicySettings), u'The `settings` field is set to type.'

    def test_configure_and_copy(self, client, policy_id):

        new_description = 'foobar'

        policy = client.policies_api.details(policy_id)

        copied_policy_id = client.policies_api.copy(policy_id)
        assert isinstance(copied_policy_id, int), u'The `copy` method returns a policy'

        copied_policy = client.policies_api.details(copied_policy_id)
        assert policy.settings.description == copied_policy.settings.description, u'The `description` field is the same'

        copied_policy.settings.description = new_description
        response = client.policies_api.configure(
            copied_policy_id,
            PolicyConfigureRequest(
                copied_policy.uuid,
                copied_policy.settings
            )
        )
        assert response is True, u'The `configure` method returns True.'

        copied_policy = client.policies_api.details(copied_policy_id)
        assert copied_policy.settings.description == new_description, u'The `description` field is the same'

        response = client.policies_api.delete(copied_policy_id)
        assert response is True, u'The `delete` method returns True.'

    def test_export_and_import(self, app, client, policy_id):
        iter_content = client.policies_api.export(policy_id, False)

        path = app.session_file_output(u'test_policies_export_and_import')
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

    def test_list(self, client, policy_id):
        # We create a policy to test get list
        assert isinstance(policy_id, int), u'Policy has been created.'
        policy_list = client.policies_api.list()
        assert isinstance(policy_list, PolicyList), u'The `list` method returns type.'
        assert isinstance(policy_list.policies[0], Policy), u'The list contains elements of type'
