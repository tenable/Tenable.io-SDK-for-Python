from tenable_io.api.base import BaseApi, BaseRequest
from tenable_io.api.models import BulkOpTask


class BulkOperationsApi(BaseApi):

    def bulk_add_agent(self, group_id, bulk_add_agent):
        """Creates a bulk operation task to add agents to a group.

        :param group_id: The agent group ID.
        :param bulk_add_agent: An instance of :class:`BulkAddAgentRequest`.
        :raise TenableIOApiException: When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.BulkOpTask`.
        """
        response = self._client.post('scanners/1/agent-groups/%(group_id)s/agents/_bulk/add',
                                     bulk_add_agent,
                                     path_params={
                                         'group_id': group_id
                                     })
        return BulkOpTask.from_json(response.text)

    def bulk_remove_agent(self, group_id, bulk_remove_agent):
        """Create a bulk operation task to remove agents from a group.

        :param group_id: The agent group ID.
        :param bulk_remove_agent: An instance of :class:`BulkRemoveAgentRequest`.
        :raise TenableIOApiException: When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.BulkOpTask`.
        """
        response = self._client.post('scanners/1/agent-groups/%(group_id)s/agents/_bulk/remove',
                                     bulk_remove_agent,
                                     path_params={
                                         'group_id': group_id
                                     })
        return BulkOpTask.from_json(response.text)

    def bulk_unlink_agent(self, bulk_unlink_agent):
        """Creates a bulk operation task to unlink (delete) agents.

        :param bulk_unlink_agent: An instance of :class:`BulkUnlinkAgentRequest`.
        :raise TenableIOApiException: When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.BulkOpTask`.
        """
        response = self._client.post('scanners/1/agents/_bulk/unlink', bulk_unlink_agent)
        return BulkOpTask.from_json(response.text)

    def bulk_agent_group_status(self, group_id, task_uuid):
        """Check the status of a bulk operation on an agent group.

        :param group_id: The agent group ID.
        :param task_uuid: The uuid of the task.
        :raise TenableIOApiException: When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.BulkOpTask`.
        """
        response = self._client.get('scanners/1/agent-groups/%(group_id)s/agents/_bulk/%(task_uuid)s',
                                    path_params={
                                        'group_id': group_id,
                                        'task_uuid': task_uuid
                                    })
        return BulkOpTask.from_json(response.text)

    def bulk_agent_status(self, task_uuid):
        """Check the status of a bulk operation on an agent.

        :param task_uuid: The uuid of the task.
        :raise TenableIOApiException: When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.BulkOpTask`.
        """
        response = self._client.get('scanners/1/agents/_bulk/%(task_uuid)s',
                                    path_params={
                                        'task_uuid': task_uuid
                                    })
        return BulkOpTask.from_json(response.text)


class BulkOpAddAgentRequest(BaseRequest):

    def __init__(
            self,
            items=None
    ):
        """Request for BulkOperationsApi.bulk_add_agent.

        :param items: list of agent ids or uuids to add to the group.
        :type items: list[int].
        """
        self.items = items


class BulkOpRemoveAgentRequest(BaseRequest):

    def __init__(
            self,
            items=None
    ):
        """Request for BulkOperationsApi.bulk_remove_agent.

        :param items: list of agent ids or uuids to add to the group.
        :type items: list[int].
        """
        self.items = items


class BulkOpUnlinkAgentRequest(BaseRequest):

    def __init__(
            self,
            items=None
    ):
        """Request for BulkOperationsApi.bulk_unlink_agent.

        :param items: list of agent ids or uuids to add to the group.
        :type items: list[int].
        """
        self.items = items
