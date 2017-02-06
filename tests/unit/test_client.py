import pytest
import six

from tenable_io.client import TenableIOClient, TenableIOApiException, TenableIORetryableApiException
from tests.base import BaseTest

if six.PY34:
    import unittest.mock as mock
else:
    import mock


class TestTenableIOClient(BaseTest):

    def test_client_retries(self):

        # Function that throws TenableIORetryableException
        mock_response = mock.Mock()
        foo = mock.Mock(side_effect=TenableIORetryableApiException(mock_response))

        # Function decoration
        retried_foo = TenableIOClient._retry(foo)

        with pytest.raises(TenableIOApiException):
            retried_foo()

        assert foo.call_count == 4, u'Should be tried 4 times (retried 3 times).'

    def test_client_throwing_retryable_exception(self):

        responses = [
            [{'status_code': 200}, False],
            [{'status_code': 429}, True],
            [{'status_code': 501}, True],
            [{'status_code': 502}, True],
            [{'status_code': 503}, True],
            [{'status_code': 504}, True],
        ]

        # Function that returns Responses with above status codes.
        foo = mock.Mock(side_effect=[mock.Mock(**response[0]) for response in responses])

        # Method decoration
        foo = TenableIOClient._error_handler(foo)

        for (response, retry) in responses:
            if retry:
                with pytest.raises(TenableIORetryableApiException):
                    foo()
            else:
                try:
                    foo()
                except TenableIORetryableApiException:
                    assert False, u'Response %s should not be retry-able.' % response
