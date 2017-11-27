import pytest

from datetime import datetime, timedelta

from tenable_io.api.agent_exclusions import AgentExclusionCreateRequest, AgentExclusionEditRequest
from tenable_io.api.models import AgentExclusion, AgentExclusionList, AgentExclusionSchedule, AgentExclusionRrules

from tests.base import BaseTest


class TestAgentExclusionsApi(BaseTest):

    @pytest.fixture(scope='class')
    def schedule_once(self):
        rrules = AgentExclusionRrules(
            "ONETIME",
            1
        )
        start_time = datetime.utcnow()
        end_time = start_time + timedelta(hours=1)

        schedule_once = AgentExclusionSchedule(
            True,
            start_time.strftime('%Y-%m-%d %H:%m:%S'),
            end_time.strftime('%Y-%m-%d %H:%m:%S'),
            'UTC',
            rrules
        )

        yield schedule_once

    @pytest.fixture(scope='class')
    def exclusion(self, app, client, schedule_once):
        """
        Create an exclusion for testing.
        """
        exclusion = client.agent_exclusions_api.create(
            AgentExclusionCreateRequest(
                app.session_name('test_agent_exclusions'),
                u'test description',
                schedule_once
            )
        )

        assert isinstance(exclusion, AgentExclusion), u'The `create` method returns type.'

        assert exclusion.schedule.enabled is True, u'Schedule must be enabled.'

        yield exclusion

        client.agent_exclusions_api.delete(exclusion.id)

    def test_create_list_delete(self, app, client):
        new_exclusion = client.agent_exclusions_api.create(
            AgentExclusionCreateRequest(
                app.session_name('test_agent_exclusions_list'),
                u'fake.tenable.com'
            )
        )
        assert isinstance(new_exclusion, AgentExclusion), u'The `create` method returns type.'

        exclusion_list = client.agent_exclusions_api.list()

        assert isinstance(exclusion_list, AgentExclusionList), u'The `list` method returns type.'

        assert len(exclusion_list.exclusions) > 0, u'Length of list cannot be 0.'

        for e in exclusion_list.exclusions:
            assert isinstance(e, AgentExclusion), u'The `list` method returns model list.'

        assert self._get_exclusion_from_exclusion_list(client, new_exclusion.id), \
            u'The created agent exclusion is present in list.'

        assert client.agent_exclusions_api.delete(new_exclusion.id), u'The `delete` method is successful.'
        assert self._get_exclusion_from_exclusion_list(client, new_exclusion.id) is None, \
            u'The deleted agent exclusion cannot be present.'

    def test_details(self, client, exclusion):
        exclusion_details = client.agent_exclusions_api.details(exclusion.id)
        assert isinstance(exclusion_details, AgentExclusion), u'The `details` method returns type.'

    def test_edit(self, app, client, exclusion):
        edited_exclusion_name = app.session_name('test_agent_exclusions_edit')
        edit_request = AgentExclusionEditRequest(
            edited_exclusion_name
        )
        edited_exclusion = client.agent_exclusions_api.edit(exclusion.id, edit_request)
        assert isinstance(edited_exclusion, AgentExclusion), u'The `edit` method returns type.'
        assert edited_exclusion.id == exclusion.id, u'Must be the same exclusion.'
        assert edited_exclusion.name == edited_exclusion_name, u'Agent exclusion name has to be edited.'

        revert_request = AgentExclusionEditRequest(
            exclusion.name
        )
        reverted_exclusion = client.agent_exclusions_api.edit(exclusion.id, revert_request)
        assert isinstance(reverted_exclusion, AgentExclusion), u'The `edit` method returns type.'
        assert reverted_exclusion.name == exclusion.name, u'AgentExclusion is reverted.'

    @staticmethod
    def _get_exclusion_from_exclusion_list(client, exclusion_id):
        exclusion_list = client.agent_exclusions_api.list()
        matching_exclusion = [e for e in exclusion_list.exclusions if e.id == exclusion_id]
        return matching_exclusion[0] if len(matching_exclusion) > 0 else None
