import pytest

from tenable_io.api.models import Session


@pytest.mark.vcr()
def test_session_get(client):
    session = client.session_api.get()
    assert isinstance(session, Session), u'The `get` method did not return type `Session`.'
