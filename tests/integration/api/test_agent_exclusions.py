import pytest

from datetime import datetime, timedelta
from random import randint

from tenable_io.api.agent_exclusions import AgentExclusionCreateRequest, AgentExclusionEditRequest
from tenable_io.api.models import AgentExclusion, AgentExclusionList, AgentExclusionSchedule, AgentExclusionRrules


def schedule_once():
    rrules = AgentExclusionRrules(
        "ONETIME",
        1
    )
    start_time = datetime.utcnow()
    end_time = start_time + timedelta(hours=1)

    return AgentExclusionSchedule(
        True,
        start_time.strftime('%Y-%m-%d %H:%m:%S'),
        end_time.strftime('%Y-%m-%d %H:%m:%S'),
        'UTC',
        rrules
    )


def create_agent_exclusion(client):
    return client.agent_exclusions_api.create(
        AgentExclusionCreateRequest(
            'test_agent_exclusion_name_{}'.format(randint(0, 100)),
            u'test description',
            schedule_once()
        )
    )

@pytest.mark.vcr()
def test_agent_exclusions_create(client):
    exclusion = create_agent_exclusion(client)
    assert isinstance(exclusion, AgentExclusion), u'The `create` method did not return type `AgentExclusion`.'

@pytest.mark.vcr()
def test_agent_exclusions_details(client):
    exclusion_details = client.agent_exclusions_api.details(create_agent_exclusion(client).id)
    assert isinstance(exclusion_details, AgentExclusion), u'The `details` method did not return type `AgentExclusion`.'

@pytest.mark.vcr()
def test_agent_exclusions_list(client):
    exclusion_list = client.agent_exclusions_api.list()
    assert isinstance(exclusion_list, AgentExclusionList), u'The `list` method did not return type `AgentExclusionList`.'

@pytest.mark.vcr()
def test_agent_exclusions_edit(client):
    exclusion = create_agent_exclusion(client)
    edited_name = 'test_agent_exclusion_name_edit_{}'.format(randint(0, 100))
    edit_request = AgentExclusionEditRequest(
        edited_name
    )
    edited_exclusion = client.agent_exclusions_api.edit(exclusion.id, edit_request)
    assert isinstance(edited_exclusion, AgentExclusion), u'The `edit` method returns type.'
    assert edited_exclusion.id == exclusion.id, u'Must be the same exclusion.'
    assert edited_exclusion.name != exclusion.name, u'Agent exclusion name has to be edited.'

@pytest.mark.vcr()
def test_agent_exclusions_delete(client):
    exclusion = create_agent_exclusion(client)
    assert client.agent_exclusions_api.delete(exclusion.id), u'Agent exclusion was not deleted.'
