from unittest.mock import Mock

import pytest

from tenable_io.client import TenableIOClient, TenableIOApiException, TenableIORetryableApiException
from tests.base import BaseTest


class TestClient(BaseTest):

    def test_client_retries(self, client):
        mock_error = Mock(side_effect=TenableIORetryableApiException(Mock()))
        retry_mock_error = TenableIOClient._retry(mock_error)
        retry_header = {u'X-Tio-Retry-Count': '3'}

        with pytest.raises(TenableIOApiException):
            retry_mock_error()

        assert mock_error.call_count == int(TenableIOClient._TOTAL_RETRIES) + 1, \
            u'Invalid retry  count: ' + str(mock_error.call_count)
        mock_error.assert_called_with(headers=retry_header)
