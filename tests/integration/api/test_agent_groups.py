import pytest

from random import randint

from tenable_io.api.agent_groups import AgentGroupSaveRequest
from tenable_io.api.models import AgentGroup, AgentGroupList, AgentList


@pytest.mark.vcr()
def test_agent_groups_create(new_agent_group):
    assert new_agent_group, u'The `create` method was not successful.'


@pytest.mark.vcr()
def test_agent_groups_list(client):
    group_list = client.agent_groups_api.list()
    assert isinstance(group_list, AgentGroupList), u'The `list` method did not return type `AgentGroupList`.'


@pytest.mark.vcr()
def test_agent_groups_details(client, new_agent_group):
    group_details = client.agent_groups_api.details(new_agent_group)
    assert isinstance(group_details, AgentGroup), u'The `details` method did not return type `AgentGroup`.'


@pytest.mark.vcr()
def test_agent_groups_agents(client, new_agent_group):
    group_agent_list = client.agent_groups_api.agents(new_agent_group)
    assert isinstance(group_agent_list, AgentList), u'The `details` method did not return type `AgentList`.'


@pytest.mark.vcr()
def test_agent_groups_delete(client, new_agent_group):
    assert client.agent_groups_api.delete(new_agent_group), u'Agent group was not deleted.'


@pytest.mark.vcr()
def test_agent_groups_add_and_remove_agent(client, new_agent_group):
    group_id = new_agent_group
    agent_list = client.agents_api.list()
    assert len(agent_list.agents) > 0, u'No agents were returned.'
    assert client.agent_groups_api.add_agent(group_id, agent_list.agents[0].id), u'Agent was added to group.'
    assert client.agent_groups_api.delete_agent(group_id, agent_list.agents[0].id), u'Agent was removed from group.'
    assert len(client.agent_groups_api.agents(group_id).agents) == 0, u'All agents were not removed.'


@pytest.mark.vcr()
def test_agent_groups_configure(client, new_agent_group):
    group_id = new_agent_group
    save_request = AgentGroupSaveRequest(
            'test_agent_group_name_edit_{}'.format(randint(0, 100))
        )
    group_details = client.agent_groups_api.details(group_id)
    assert client.agent_groups_api.configure(group_id, save_request), u'The `configure` request was not successful.'
    edited_group_details = client.agent_groups_api.details(group_id)
    assert group_details.name != edited_group_details.name, u'The Agent group name was not edited.'
