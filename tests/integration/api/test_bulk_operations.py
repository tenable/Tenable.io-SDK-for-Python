import pytest

from tenable_io.api.bulk_operations import BulkOpAddAgentRequest, BulkOpRemoveAgentRequest, BulkOpUnlinkAgentRequest
from tenable_io.api.models import BulkOpTask


@pytest.mark.vcr()
def test_bulk_operations_bulk_agent_add_and_status(client, new_agent_group, fetch_agent):
    add_agent_task = client.bulk_operations_api.bulk_add_agent(
        new_agent_group,
        BulkOpAddAgentRequest(
            items=[fetch_agent]
        )
    )
    assert isinstance(add_agent_task, BulkOpTask), u'The `bulk_add_agent` method did not return type `BulkOpTask`.'
    agent_status = client.bulk_operations_api.bulk_agent_status(add_agent_task.task_id)
    assert isinstance(agent_status,
                      BulkOpTask), u'The `bulk_agent_status` method did not return type `BulkOpTask`.'

@pytest.mark.vcr()
def test_bulk_operations_bulk_agent_remove_and_status(client, new_agent_group, fetch_agent):
    remove_agent_task = client.bulk_operations_api.bulk_remove_agent(
        new_agent_group,
        BulkOpRemoveAgentRequest(
            items=[fetch_agent]
        )
    )
    assert isinstance(remove_agent_task,
                      BulkOpTask), u'The `bulk_remove_agent` method did not return type `BulkOpTask`.'
    group_status = client.bulk_operations_api.bulk_agent_group_status(new_agent_group, remove_agent_task.task_id)
    assert isinstance(group_status,
                      BulkOpTask), u'The `bulk_agent_group_status` method did not return type `BulkOpTask`.'

@pytest.mark.vcr()
def test_bulk_operations_bulk_agent_unlink(client, fetch_agent):
    unlink_agent_task = client.bulk_operations_api.bulk_unlink_agent(
        BulkOpUnlinkAgentRequest(items=[fetch_agent]))
    assert isinstance(unlink_agent_task,
                      BulkOpTask), u'The `bulk_unlink_agent` method did not return type `BulkOpTask`.'
