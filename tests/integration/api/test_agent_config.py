import pytest

from tenable_io.api.agent_config import AgentConfigRequest
from tenable_io.api.models import AgentConfig

from tests.base import BaseTest


class TestAgentConfigApi(BaseTest):

    def test_details_edit(self, client):
        # Get agent config details.
        previous_config = client.agent_config_api.details()
        assert isinstance(previous_config, AgentConfig), u'Details request returns type AgentConfig.'

        # Edit agent config to new value.
        previous_expiration = previous_config.auto_unlink['expiration']
        new_expiration = 10 if previous_expiration >= 365 else previous_expiration + 1

        self._edit_config(client, AgentConfigRequest(
            software_update=not previous_config.software_update,
            auto_unlink={
                'enabled': not previous_config.auto_unlink['enabled'],
                'expiration': new_expiration
            }
        ))

        # Edit agent config to previous value.
        self._edit_config(client, AgentConfigRequest(
            software_update=previous_config.software_update,
            auto_unlink={
                'enabled': previous_config.auto_unlink['enabled'],
                'expiration': previous_expiration
            }
        ))

        # Get agent config details to test if values reverted back.
        reverted_config = client.agent_config_api.details()
        self._assert_response(
            expected=previous_config,
            response=reverted_config,
            error_text=u'Edit config response returns correct values.'
        )

    def _edit_config(self, client, agent_config_request):
        edit_response = client.agent_config_api.edit(agent_config_request)
        self._assert_response(
            expected=agent_config_request,
            response=edit_response,
            error_text=u'Edit config response returns correct values.'
        )

    @staticmethod
    def _assert_response(expected, response, error_text):
        assert isinstance(response, AgentConfig), u'Response returns type AgentConfig.'
        assert response.software_update == expected.software_update \
            and response.auto_unlink['enabled'] == expected.auto_unlink['enabled'] \
            and response.auto_unlink['expiration'] == expected.auto_unlink['expiration'], \
            error_text
