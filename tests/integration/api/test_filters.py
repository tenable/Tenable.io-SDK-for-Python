from tenable_io.api.models import Filter, Filters

from tests.base import BaseTest


class TestFiltersApi(BaseTest):

    def test_agents_filters(self, client):
        agents_filters = client.filters_api.agents_filters()

        assert isinstance(agents_filters, Filters), u'Agent filters request returns type.'
        for f in agents_filters.filters:
            assert isinstance(f, Filter), u'Filters property represents type.'
