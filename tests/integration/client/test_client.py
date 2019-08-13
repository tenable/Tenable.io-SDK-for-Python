import pytest

from tenable_io.client import TenableIOClient
from tenable_io.exceptions import TenableIOApiException, TenableIOErrorCode
from tests.base import BaseTest


class TestTenableIOClient(BaseTest):

    @pytest.mark.vcr()
    def test_client_bad_keys(self):
        try:
            TenableIOClient('bad', 'key').session_api.get()
            assert False, u'TenableIOApiException should be raised for bad api and secret keys.'
        except TenableIOApiException as e:
            assert e.code is TenableIOErrorCode.UNAUTHORIZED, u'Appropriate exception is raised.'
