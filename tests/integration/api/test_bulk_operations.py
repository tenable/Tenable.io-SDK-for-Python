import pytest

from tenable_io.api.agent_groups import AgentGroupSaveRequest
from tenable_io.api.bulk_operations import BulkOpAddAgentRequest, BulkOpRemoveAgentRequest, BulkOpUnlinkAgentRequest
from tenable_io.api.models import AgentList, BulkOpTask

from tests.base import BaseTest


class TestBulkOperationsApi(BaseTest):

    @pytest.fixture(scope='class')
    def agent_group_id(self, app, client):
        """
        Create an agent group for testing.
        """
        # Create agent group for testing.
        agent_group_name = app.session_name('test_bulk_add_agent')
        agent_group_id = client.agent_groups_api.create(
            AgentGroupSaveRequest(
                agent_group_name
            )
        )
        assert agent_group_id, u'Create request returns valid ID.'

        yield agent_group_id

        # Delete the newly created agent group
        client.agent_groups_api.delete(agent_group_id)

    @pytest.fixture(scope='class')
    def agent_id(self, client):
        """
        Returns id of first agent in list for testing.
        """
        agent_list = client.agents_api.list()

        assert isinstance(agent_list, AgentList)

        yield agent_list.agents[0].id if len(agent_list.agents) > 0 else None

    def test_bulk_agent_status_add_remove_group(self, client, agent_group_id, agent_id):

        if agent_id is not None:
            # Create task to bulk add agent to specified agent group
            add_agent_task = client.bulk_operations_api.bulk_add_agent(
                agent_group_id,
                BulkOpAddAgentRequest(
                    items=[agent_id]
                )
            )
            assert isinstance(add_agent_task, BulkOpTask), u'Bulk add agent request returns type.'

            # Test bulk agent status
            add_agent_task = self.wait_until(
                lambda: client.bulk_operations_api.bulk_agent_status(add_agent_task.task_id),
                lambda task: task.status in [BulkOpTask.STATUS_COMPLETED]
            )
            assert isinstance(add_agent_task, BulkOpTask), u'Bulk agent status request returns type.'
            assert add_agent_task.status == BulkOpTask.STATUS_COMPLETED, u'Bulk add agent task is completed.'

            # Ensure agent is indeed added to the specified agent group
            agent_list = client.agent_groups_api.agents(agent_group_id)
            assert isinstance(agent_list, AgentList), u'Agent list request returns type.'
            test_agent = [a for a in agent_list.agents if a.id == agent_id]
            assert len(test_agent) == 1, u'Newly added agent exist in agent group.'

            # Create task to bulk remove agent from specified agent group
            remove_agent_task = client.bulk_operations_api.bulk_remove_agent(
                agent_group_id,
                BulkOpRemoveAgentRequest(
                    items=[agent_id]
                )
            )
            assert isinstance(remove_agent_task, BulkOpTask), u'Bulk remove agent request returns type.'

            # Test bulk agent group status
            remove_agent_task = self.wait_until(
                lambda: client.bulk_operations_api.bulk_agent_group_status(agent_group_id, remove_agent_task.task_id),
                lambda task: task.status in [BulkOpTask.STATUS_COMPLETED]
            )
            assert isinstance(remove_agent_task, BulkOpTask), u'Bulk agent group status request returns type.'
            assert remove_agent_task.status == BulkOpTask.STATUS_COMPLETED, u'Bulk add agent task is completed.'

            # Ensure agent is indeed removed from specified agent group
            agent_list = client.agent_groups_api.agents(agent_group_id)
            test_agent = [a for a in agent_list.agents if a.id == agent_id]
            assert len(test_agent) == 0, u'Newly added agent is removed from agent group.'

    def test_bulk_unlink_agent(self, client):
        # Test existence of api, task is created to fail with string agent id in items list
        unlink_agent_task = client.bulk_operations_api.bulk_unlink_agent(
            BulkOpUnlinkAgentRequest(items=['test_bulk_unlink_agent']))
        assert isinstance(unlink_agent_task, BulkOpTask), u'Bulk unlink agent request returns type.'
