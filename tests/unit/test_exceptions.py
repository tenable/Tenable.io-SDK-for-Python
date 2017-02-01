from tenable_io.exceptions import TenableIOErrorCode, TenableIOException
from tests.base import BaseTest


class TestTenableIOException(BaseTest):

    def test_default_error_code_not_none(self):
        exception = TenableIOException()
        assert exception.code is not None, u'There should always be a code.'
        exception2 = TenableIOException(code=None)
        assert exception2.code is not None, u'Error code is never None even if None is passed as code in constructor.'

    def test_default_error_code_is_generic(self):
        exception = TenableIOException()
        assert exception.code is TenableIOErrorCode.GENERIC, u'Default error code should be generic.'


class TestTenableIOErrorCode(BaseTest):

    def test_from_http_code(self):
        assert TenableIOErrorCode.from_http_code(404) is not None, u'Error code found for 404 http status code.'
        assert TenableIOErrorCode.from_http_code(429) is TenableIOErrorCode.TOO_MANY_REQUESTS, \
            u'Error code "TOO MANY REQUEST" is found for 429 http status code.'
