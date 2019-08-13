import pytest

from tenable_io.api.models import ServerProperties, ServerStatus


@pytest.mark.vcr()
def test_server_properties(client):
    server_properties = client.server_api.properties()
    assert isinstance(server_properties, ServerProperties), \
        u'The `properties` method did not return type `ServerProperties`.'


@pytest.mark.vcr()
def test_server_status(client):
    server_status = client.server_api.status()
    assert isinstance(server_status, ServerStatus), u'The `status` method did not return type `ServerStatus`.'
