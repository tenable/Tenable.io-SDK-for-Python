from json import loads

from tenable_io.api.base import BaseApi, BaseRequest
from tenable_io.api.models import AgentGroup, AgentGroupList, AgentList


class AgentGroupsApi(BaseApi):

    def add_agent(self, agent_group_id, agent_id, scanner_id=1):
        """Add an agent to the given agent group.

        :param agent_group_id: The agent group ID.
        :param agent_id: The agent ID.
        :param scanner_id: The scanner ID.
        :raise TenableIOApiException: When API error is encountered.
        :return: True if successful.
        """
        self._client.put('scanners/%(scanner_id)s/agent-groups/%(agent_group_id)s/agents/%(agent_id)s',
                         path_params={
                             'scanner_id': scanner_id,
                             'agent_group_id': agent_group_id,
                             'agent_id': agent_id
                         })
        return True

    def agents(
            self,
            agent_group_id,
            scanner_id=1,
            offset=None,
            limit=None,
            sort=None,
            f=None,
            ft=None,
            w=None,
            wf=None
    ):
        """Get agent list for given agent group.

        :param agent_group_id: The agent group ID.
        :param scanner_id: The scanner ID.
        :param offset: The starting record to retrieve, defaults to 0 if not defined.
        :param limit: The number of records to retrieve, API will defaults to 50 if not defined.
        :param sort: The sort order of the returned records.
        :param f: Apply a filter in the format '<field_name>:<operation>:<value>'.
        :param ft: Filter type. ("and" or "or").
        :param w: Wildcard filter text.
        :param wf: A comma delimited subset of wildcard_fields to search when applying the wildcard filter.
        :raise TenableIOApiException: When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.AgentList`.
        """
        params = {
            'offset': offset,
            'limit': limit,
            'sort': sort,
            'f': f,
            'ft': ft,
            'w': w,
            'wf': wf
        }
        params = {k: v for k, v in params.items() if v is not None}
        response = self._client.get('scanners/%(scanner_id)s/agent-groups/%(agent_group_id)s/agents',
                                    path_params={
                                        'scanner_id': scanner_id,
                                        'agent_group_id': agent_group_id
                                    },
                                    params=params)
        return AgentList.from_json(response.text)

    def configure(self, agent_group_id, configure_agent_group, scanner_id=1):
        """Configure name of give agent group.

        :param agent_group_id: The agent group ID.
        :param scanner_id: The scanner ID.
        :param configure_agent_group: An instance of :class:`AgentGroupSaveRequest`.
        :raise TenableIOApiException: When API error is encountered.
        :return: True if successful.
        """
        self._client.put('scanners/%(scanner_id)s/agent-groups/%(agent_group_id)s',
                         configure_agent_group,
                         path_params={
                             'scanner_id': scanner_id,
                             'agent_group_id': agent_group_id
                         })
        return True

    def create(self, create_agent_group, scanner_id=1):
        """Create an agent group.

        :param create_agent_group: An instance of :class:`AgentGroupSaveRequest`.
        :param scanner_id: The scanner ID.
        :raise TenableIOApiException: When API error is encountered.
        :return: The ID of agent group just created.
        """
        response = self._client.post('scanners/%(scanner_id)s/agent-groups',
                                     create_agent_group,
                                     path_params={
                                         'scanner_id': scanner_id
                                     })
        return loads(response.text).get('id')

    def delete(self, agent_group_id, scanner_id=1):
        """Delete an agent group.

        :param agent_group_id: The agent group ID.
        :param scanner_id: The scanner ID.
        :raise TenableIOApiException: When API error is encountered.
        :return: True if successful.
        """
        self._client.delete('scanners/%(scanner_id)s/agent-groups/%(agent_group_id)s',
                            path_params={
                                'scanner_id': scanner_id,
                                'agent_group_id': agent_group_id
                            })
        return True

    def delete_agent(self, agent_group_id, agent_id, scanner_id=1):
        """Delete an agent from the given agent group.

        :param agent_group_id: The agent group ID.
        :param agent_id: The agent ID.
        :param scanner_id: The scanner ID.
        :raise TenableIOApiException: When API error is encountered.
        :return: True if successful.
        """
        self._client.delete('scanners/%(scanner_id)s/agent-groups/%(agent_group_id)s/agents/%(agent_id)s',
                            path_params={
                                'scanner_id': scanner_id,
                                'agent_group_id': agent_group_id,
                                'agent_id': agent_id
                            })
        return True

    def details(
            self,
            agent_group_id,
            scanner_id=1,
            offset=None,
            limit=None,
            sort=None,
            f=None,
            ft=None,
            w=None,
            wf=None
    ):
        """Get details of given agent group.

        :param agent_group_id: The agent group ID.
        :param scanner_id: The scanner ID.
        :param offset: The starting record to retrieve, defaults to 0 if not defined.
        :param limit: The number of records to retrieve, API will defaults to 50 if not defined.
        :param sort: The sort order of the returned records.
        :param f: Apply a filter in the format '<field_name>:<operation>:<value>'.
        :param ft: Filter type. ("and" or "or").
        :param w: Wildcard filter text.
        :param wf: A comma delimited subset of wildcard_fields to search when applying the wildcard filter.
        :raise TenableIOApiException: When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.AgentGroup`.
        """
        params = {
            'offset': offset,
            'limit': limit,
            'sort': sort,
            'f': f,
            'ft': ft,
            'w': w,
            'wf': wf
        }
        params = {k: v for k, v in params.items() if v is not None}
        response = self._client.get('scanners/%(scanner_id)s/agent-groups/%(agent_group_id)s',
                                    path_params={
                                        'scanner_id': scanner_id,
                                        'agent_group_id': agent_group_id
                                    },
                                    params=params)
        return AgentGroup.from_json(response.text)

    def list(self, scanner_id=1):
        """Return agent groups for the given scanner.

        :param scanner_id: The scanner ID.
        :raise TenableIOApiException: When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.AgentGroupList`.
        """
        response = self._client.get('scanners/%(scanner_id)s/agent-groups',
                                    path_params={
                                        'scanner_id': scanner_id
                                    })
        return AgentGroupList.from_json(response.text)


class AgentGroupSaveRequest(BaseRequest):

    def __init__(
            self,
            name
    ):
        self.name = name
