from tenable_io.api.base import BaseApi
from tenable_io.api.models import AgentList


class AgentsApi(BaseApi):

    def delete(self, agent_id):
        """Deletes the given agent.

        :param agent_id: The Agent ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.delete('scanners/1/agents/%(agent_id)s', path_params={'agent_id': agent_id})
        return True

    def list(self, offset=None, limit=None):
        """Lists agents for the given scanner.

        :param offset: The starting record to retrieve, defaults to 0 if not defined.
        :param limit: The number of records to retrieve, API will defaults to 50 if not defined.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.AgentList`.
        """
        params = {}
        if offset is not None:
            params['offset'] = offset
        if limit is not None:
            params['limit'] = limit
        response = self._client.get('scanners/1/agents', params=params)
        return AgentList.from_json(response.text)
