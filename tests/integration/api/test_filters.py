import pytest

from tenable_io.api.models import Filter, Filters


@pytest.mark.vcr()
def test_agents_filters(client):
    agents_filters = client.filters_api.agents_filters()

    assert isinstance(agents_filters, Filters), u'The `agents_filters` method return did not return type `Filters`.'
    for f in agents_filters.filters:
        assert isinstance(f, Filter), u'filters property should contain `Filter` type.'