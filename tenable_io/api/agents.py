from tenable_io.api.base import BaseApi
from tenable_io.api.models import AgentList, Agent


class AgentsApi(BaseApi):

    def delete(self, agent_id):
        """Deletes the given agent.

        :param agent_id: The Agent ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.delete('scanners/1/agents/%(agent_id)s', path_params={'agent_id': agent_id})
        return True

    def list(self, offset=None, limit=None, sort=None, f=None, ft=None, w=None, wf=None):
        """Lists agents for the given scanner.

        :param offset: The starting record to retrieve, defaults to 0 if not defined.
        :param limit: The number of records to retrieve, API will defaults to 50 if not defined.
        :param sort: The sort order of the returned records.
        :param f: Apply a filter in the format '<field_name>:<operation>:<value>'.
        :param ft: Filter type. ("and" or "or").
        :param w: Wildcard filter text.
        :param wf: A comma delimited subset of wildcard_fields to search when applying the wildcard filter.
        :raise TenableIOApiException:  When API error is encountered.
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
        response = self._client.get('scanners/1/agents', params=params, flatten_params=False)
        return AgentList.from_json(response.text)

    def get(self, agent_id):
        """Get the given agent.

        :param agent_id: The Agent ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.Agent`.
        """
        response = self._client.get('scanners/1/agents/%(agent_id)s', path_params={'agent_id': agent_id})
        return Agent.from_json(response.text)
