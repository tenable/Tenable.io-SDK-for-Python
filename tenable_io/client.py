import requests
import sys

from requests.utils import quote
from time import sleep

from tenable_io.config import TenableIOConfig
from tenable_io.exceptions import TenableIOApiException, TenableIORetryableApiException
from tenable_io.api.base import BaseRequest
from tenable_io.api.editor import EditorApi
from tenable_io.api.exclusions import ExclusionApi
from tenable_io.api.file import FileApi
from tenable_io.api.folders import FoldersApi
from tenable_io.api.groups import GroupsApi
from tenable_io.api.plugins import PluginsApi
from tenable_io.api.policies import PoliciesApi
from tenable_io.api.scans import ScansApi
from tenable_io.api.scanners import ScannersApi
from tenable_io.api.server import ServerApi
from tenable_io.api.session import SessionApi
from tenable_io.api.target_groups import TargetGroupsApi
from tenable_io.api.users import UsersApi
from tenable_io.helpers.folder import FolderHelper
from tenable_io.helpers.policy import PolicyHelper
from tenable_io.helpers.scan import ScanHelper
from tenable_io.log import logging


class TenableIOClient(object):

    MAX_RETRIES = 3
    RETRY_SLEEP_MILLISECONDS = 500

    def __init__(
            self,
            access_key=TenableIOConfig.get('access_key'),
            secret_key=TenableIOConfig.get('secret_key'),
            endpoint=TenableIOConfig.get('endpoint'),
    ):
        self._access_key = access_key
        self._secret_key = secret_key
        self._endpoint = endpoint

        self._headers = {
            u'X-ApiKeys': u'accessKey=%s; secretKey=%s;' % (self._access_key, self._secret_key),
            u'User-Agent': u'TenableIOSDK Python/%s' % ('.'.join([str(i) for i in sys.version_info][0:3]))
        }

        self._ini_api()
        self._init_helpers()

    def _ini_api(self):
        """
        Initialize all api.
        """
        self.editor_api = EditorApi(self)
        self.exclusions_api = ExclusionApi(self)
        self.file_api = FileApi(self)
        self.folders_api = FoldersApi(self)
        self.groups_api = GroupsApi(self)
        self.plugins_api = PluginsApi(self)
        self.policies_api = PoliciesApi(self)
        self.scans_api = ScansApi(self)
        self.scanners_api = ScannersApi(self)
        self.server_api = ServerApi(self)
        self.session_api = SessionApi(self)
        self.target_groups_api = TargetGroupsApi(self)
        self.users_api = UsersApi(self)

    def _init_helpers(self):
        """
        Initialize all helpers.
        """
        self.policy_helper = PolicyHelper(self)
        self.scan_helper = ScanHelper(self)
        self.folder_helper = FolderHelper(self)

    def _retry(f):
        """
        Decorator to retry when TenableIORetryableException is caught.
        :param f: Method to retry.
        :return: A decorated method that implicitly retry the original method upon \
        TenableIORetryableException is caught.
        """
        def wrapper(*args, **kwargs):
            count = 0
            retry = True
            sleep_ms = 0

            while retry:
                retry = False
                try:
                    return f(*args, **kwargs)
                except TenableIORetryableApiException as exception:
                    count += 1

                    if count <= TenableIOClient.MAX_RETRIES:
                        retry = True
                        sleep_ms += count * TenableIOClient.RETRY_SLEEP_MILLISECONDS
                        logging.warn(u'Retry %d of %d. Sleep %dms' % (count, TenableIOClient.MAX_RETRIES, sleep_ms))
                        sleep(sleep_ms / 1000.0)
                    else:
                        raise TenableIOApiException(exception.response)

        return wrapper

    def _error_handler(f):
        """
        Decorator to handle response error.
        :param f: Response returning method.
        :return: A Response returning method that raises TenableIOException for error in response.
        """
        def wrapper(*args, **kwargs):
            response = f(*args, **kwargs)

            if response.status_code == 429:
                raise TenableIORetryableApiException(response)
            if response.status_code in [501, 502, 503, 504]:
                raise TenableIORetryableApiException(response)
            if not 200 <= response.status_code <= 299:
                raise TenableIOApiException(response)

            return response
        return wrapper

    @_retry
    @_error_handler
    def get(self, uri, path_params=None, **kwargs):
        return self._request('GET', uri, path_params, **kwargs)

    @_retry
    @_error_handler
    def post(self, uri, payload=None, path_params=None, **kwargs):
        if isinstance(payload, BaseRequest):
            payload = payload.as_payload()
        return self._request('POST', uri, path_params, json=payload, **kwargs)

    @_retry
    @_error_handler
    def put(self, uri, payload=None, path_params=None, **kwargs):
        if isinstance(payload, BaseRequest):
            payload = payload.as_payload()
        return self._request('PUT', uri, path_params, json=payload, **kwargs)

    @_retry
    @_error_handler
    def delete(self, uri, path_params=None, **kwargs):
        return self._request('DELETE', uri, path_params, **kwargs)

    def _request(self, method, uri, path_params=None, **kwargs):
        if path_params:
            # Ensure path param is encoded.
            path_params = {key: quote(str(value), safe=u'') for key, value in path_params.items()}
            uri %= path_params

        full_uri = self._endpoint + uri
        logging.debug(u'API Request: %s %s %s' % (method, full_uri, kwargs))

        response = requests.request(method, full_uri, headers=self._headers, **kwargs)
        log_message = u'API Response: %s %s %s %s %s %s' % (response.request.method, response.url, response.reason,
                                                            ('status_code', response.status_code),
                                                            response.headers.get('x-gateway-site-id'),
                                                            response.headers.get('x-request-uuid'))
        logging.debug(log_message)
        if not 200 <= response.status_code <= 299:
            logging.error(log_message)

        return response

    # Delayed qualifying decorator as staticmethod. This is a workaround to error raised from using a decorator
    # decorated by @staticmethod.
    _retry = staticmethod(_retry)
    _error_handler = staticmethod(_error_handler)
