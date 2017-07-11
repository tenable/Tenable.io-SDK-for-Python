import json
import pytest

from tests.base import BaseTest

from tenable_io.api.models import ScContainer
from tenable_io.exceptions import TenableIOApiException


class TestScContainersApi(BaseTest):

    def test_delete(self, client):
        with pytest.raises(TenableIOApiException) as e:
            client.sc_containers_api.delete(u'test_sc_containers', u'test_sc_containers')
        assert e.value.response.status_code == 404, u'Request cannot return with 404.'
        assert json.loads(e.value.response.text)[u'status'] == u'digest_not_found'

    def test_list(self, client):
        containers = client.sc_containers_api.list()
        if len(containers) > 0:
            assert isinstance(containers[0], ScContainer), u'The method returns container list.'
