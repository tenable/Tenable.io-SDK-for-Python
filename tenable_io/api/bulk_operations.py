from tenable_io.api.base import BaseApi, BaseRequest
from tenable_io.api.models import BulkOpTask


class BulkOperationsApi(BaseApi):

    def bulk_add_agent(self, group_id, bulk_add_agent, scanner_id=1):
        """Creates a bulk operation task to add agents to a group.

        :param group_id: The agent group ID.
        :param bulk_add_agent: An instance of :class:`BulkAddAgentRequest`.
        :param scanner_id: The scanner ID.
        :raise TenableIOApiException: When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.BulkOpTask`.
        """
        response = self._client.post('scanners/%(scanner_id)s/agent-groups/%(group_id)s/agents/_bulk/add',
                                     bulk_add_agent,
                                     path_params={
                                         'scanner_id': scanner_id,
                                         'group_id': group_id
                                     })
        return BulkOpTask.from_json(response.text)

    def bulk_remove_agent(self, group_id, bulk_remove_agent, scanner_id=1):
        """Create a bulk operation task to remove agents from a group.

        :param group_id: The agent group ID.
        :param bulk_remove_agent: An instance of :class:`BulkRemoveAgentRequest`.
        :param scanner_id: The scanner ID.
        :raise TenableIOApiException: When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.BulkOpTask`.
        """
        response = self._client.post('scanners/%(scanner_id)s/agent-groups/%(group_id)s/agents/_bulk/remove',
                                     bulk_remove_agent,
                                     path_params={
                                         'scanner_id': scanner_id,
                                         'group_id': group_id
                                     })
        return BulkOpTask.from_json(response.text)

    def bulk_unlink_agent(self, bulk_unlink_agent, scanner_id=1):
        """Creates a bulk operation task to unlink (delete) agents.

        :param bulk_unlink_agent: An instance of :class:`BulkUnlinkAgentRequest`.
        :param scanner_id: The scanner ID.
        :raise TenableIOApiException: When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.BulkOpTask`.
        """
        response = self._client.post('scanners/%(scanner_id)s/agents/_bulk/unlink',
                                     bulk_unlink_agent,
                                     path_params={
                                         'scanner_id': scanner_id,
                                     })
        return BulkOpTask.from_json(response.text)

    def bulk_agent_group_status(self, group_id, task_uuid, scanner_id=1):
        """Check the status of a bulk operation on an agent group.

        :param group_id: The agent group ID.
        :param task_uuid: The uuid of the task.
        :param scanner_id: The scanner ID.
        :raise TenableIOApiException: When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.BulkOpTask`.
        """
        response = self._client.get('scanners/%(scanner_id)s/agent-groups/%(group_id)s/agents/_bulk/%(task_uuid)s',
                                    path_params={
                                        'scanner_id': scanner_id,
                                        'group_id': group_id,
                                        'task_uuid': task_uuid
                                    })
        return BulkOpTask.from_json(response.text)

    def bulk_agent_status(self, task_uuid, scanner_id=1):
        """Check the status of a bulk operation on an agent.

        :param task_uuid: The uuid of the task.
        :param scanner_id: The scanner ID.
        :raise TenableIOApiException: When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.BulkOpTask`.
        """
        response = self._client.get('scanners/%(scanner_id)s/agents/_bulk/%(task_uuid)s',
                                    path_params={
                                        'scanner_id': scanner_id,
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
