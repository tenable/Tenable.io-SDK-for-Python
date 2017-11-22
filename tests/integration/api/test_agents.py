from tenable_io.api.models import Agent, AgentList, FilterPagination, FilterSort
from tenable_io.exceptions import TenableIOApiException, TenableIOErrorCode

from tests.base import BaseTest


class TestAgentsApi(BaseTest):

    def test_delete(self, client):
        try:
            client.agents_api.delete('test_agents_delete')
        except TenableIOApiException as e:
            assert e.code in (TenableIOErrorCode.BAD_REQUEST, TenableIOErrorCode.NOT_FOUND), \
                u'Bad request for string agent_id or agent not found.'

    def test_list(self, client):
        agent_list = client.agents_api.list()
        assert isinstance(agent_list, AgentList), u'List request returns type.'
        for a in agent_list.agents:
            assert isinstance(a, Agent), u'Agents property represents type.'

        assert isinstance(agent_list.pagination, FilterPagination), u'Pagination property represents type.'
        for s in agent_list.pagination.sort:
            assert isinstance(s, FilterSort), u'Sort property represents type.'
