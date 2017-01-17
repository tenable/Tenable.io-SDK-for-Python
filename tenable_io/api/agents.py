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

    def list(self):
        """Lists agents for the given scanner.

        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.AgentList`.
        """
        response = self._client.get('scanners/1/agents')
        return AgentList.from_json(response.text)
