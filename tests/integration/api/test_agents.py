import pytest

from tenable_io.api.models import Agent, AgentList


@pytest.mark.vcr()
def test_agents_list(client):
    agent_list = client.agents_api.list(limit=2)
    assert isinstance(agent_list, AgentList), u'The `list` method did not return type `AgentList`.'
    assert len(agent_list.agents) == 2, u'Expected limit to be applied.'
    for a in agent_list.agents:
        assert isinstance(a, Agent), u'Agents property does not represent type.'


@pytest.mark.vcr()
def test_agents_get(client):
    agent_list = client.agents_api.list()
    assert len(agent_list.agents) > 0, u'Expected at least one agent.'
    agent = client.agents_api.get(agent_list.agents[0].id)
    assert isinstance(agent, Agent), u'The `get` method did not return type `AgentList`.'


@pytest.mark.vcr()
def test_agents_delete(client):
    agent_list = client.agents_api.list()
    assert len(agent_list.agents) > 0, u'Expected at least one agent.'
    assert client.agents_api.delete(agent_list.agents[0].id), u'The Agent was not deleted.'
