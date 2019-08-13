import pytest

from tenable_io.api.agent_config import AgentConfigRequest
from tenable_io.api.models import AgentConfig

@pytest.mark.vcr()
def test_agent_config_get_details(client):
    config = client.agent_config_api.details()
    assert isinstance(config, AgentConfig), u'The `details` method did not return type `AgentConfig`.'


@pytest.mark.vcr()
def test_agent_config_edit(client):
    config = client.agent_config_api.details()
    assert isinstance(config, AgentConfig), u'The `details` method did not return type `AgentConfig`.'

    # Edit agent config to new value.
    previous_expiration = config.auto_unlink['expiration']
    new_expiration = 10 if config.auto_unlink['expiration'] >= 365 else config.auto_unlink['expiration'] + 1

    edit_config = client.agent_config_api.edit(AgentConfigRequest(
        software_update=not config.software_update,
        auto_unlink={
            'enabled': not config.auto_unlink['enabled'],
            'expiration': new_expiration
        }
    ))
    assert isinstance(edit_config, AgentConfig), u'The `edit` method did not return type `AgentConfig`.'

    # Edit agent config to previous value.
    final_config = client.agent_config_api.edit(AgentConfigRequest(
        software_update=config.software_update,
        auto_unlink={
            'enabled': config.auto_unlink['enabled'],
            'expiration': previous_expiration
        }
    ))
    assert isinstance(final_config, AgentConfig), u'The `edit` method did not return type `AgentConfig`.'
    assert final_config.auto_unlink == config.auto_unlink, u'Final config should match original config.'
