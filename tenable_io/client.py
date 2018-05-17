import requests
import sys
from time import sleep

from requests.utils import quote

from tenable_io.config import TenableIOConfig
from tenable_io.exceptions import TenableIOApiException, TenableIORetryableApiException
from tenable_io.api.agent_exclusions import AgentExclusionsApi
from tenable_io.api.agent_config import AgentConfigApi
from tenable_io.api.agent_groups import AgentGroupsApi
from tenable_io.api.agents import AgentsApi
from tenable_io.api.assets import AssetsApi
from tenable_io.api.base import BaseRequest
from tenable_io.api.bulk_operations import BulkOperationsApi
from tenable_io.api.editor import EditorApi
from tenable_io.api.exclusions import ExclusionApi
from tenable_io.api.file import FileApi
from tenable_io.api.filters import FiltersApi
from tenable_io.api.folders import FoldersApi
from tenable_io.api.groups import GroupsApi
from tenable_io.api.import_ import ImportApi
from tenable_io.api.plugins import PluginsApi
from tenable_io.api.policies import PoliciesApi
from tenable_io.api.scans import ScansApi
from tenable_io.api.scanners import ScannersApi
from tenable_io.api.sc_containers import ScContainersApi
from tenable_io.api.sc_policy import ScPolicyApi
from tenable_io.api.sc_reports import ScReportsApi
from tenable_io.api.sc_test_jobs import ScTestJobsApi
from tenable_io.api.server import ServerApi
from tenable_io.api.session import SessionApi
from tenable_io.api.target_groups import TargetGroupsApi
from tenable_io.api.users import UsersApi
from tenable_io.api.workbenches import WorkbenchesApi
from tenable_io.helpers.file import FileHelper
from tenable_io.helpers.folder import FolderHelper
from tenable_io.helpers.permissions import PermissionsHelper
from tenable_io.helpers.policy import PolicyHelper
from tenable_io.helpers.scan import ScanHelper
from tenable_io.helpers.workbench import WorkbenchHelper
from tenable_io.log import format_request, logging


class TenableIOClient(object):

    _MAX_RETRIES = TenableIOConfig.get('max_retries')
    _TOTAL_RETRIES = _MAX_RETRIES if int(_MAX_RETRIES) < 5 else 5
    _RETRY_STATUS_CODES = {429, 500, 501, 502, 503, 504}
    _RETRY_SLEEP_MILLISECONDS = TenableIOConfig.get('retry_sleep_milliseconds')

    def __init__(
            self,
            access_key=TenableIOConfig.get('access_key'),
            secret_key=TenableIOConfig.get('secret_key'),
            endpoint=TenableIOConfig.get('endpoint'),
            impersonate=None,
    ):
        self._access_key = access_key
        self._secret_key = secret_key
        self._endpoint = endpoint
        self._impersonate = impersonate

        self._init_session()
        self._init_api()
        self._init_helpers()

    def _init_session(self):
        """
        Initializes the requests session
        """
        self._session = requests.Session()
        self._session.headers.update({
            u'X-ApiKeys': u'accessKey=%s; secretKey=%s;' % (self._access_key, self._secret_key),
            u'User-Agent': u'TenableIOSDK Python/%s' % ('.'.join([str(i) for i in sys.version_info][0:3]))
        })
        if self._impersonate:
            self._session.headers.update({
                u'X-Impersonate': u'username=%s' % self._impersonate
            })

    def _init_api(self):
        """
        Initializes all api.
        """
        self.agent_exclusions_api = AgentExclusionsApi(self)
        self.agent_config_api = AgentConfigApi(self)
        self.agent_groups_api = AgentGroupsApi(self)
        self.agents_api = AgentsApi(self)
        self.assets_api = AssetsApi(self)
        self.bulk_operations_api = BulkOperationsApi(self)
        self.editor_api = EditorApi(self)
        self.exclusions_api = ExclusionApi(self)
        self.file_api = FileApi(self)
        self.filters_api = FiltersApi(self)
        self.folders_api = FoldersApi(self)
        self.groups_api = GroupsApi(self)
        self.import_api = ImportApi(self)
        self.plugins_api = PluginsApi(self)
        self.policies_api = PoliciesApi(self)
        self.scans_api = ScansApi(self)
        self.scanners_api = ScannersApi(self)
        self.sc_containers_api = ScContainersApi(self)
        self.sc_policy_api = ScPolicyApi(self)
        self.sc_reports_api = ScReportsApi(self)
        self.sc_test_jobs_api = ScTestJobsApi(self)
        self.server_api = ServerApi(self)
        self.session_api = SessionApi(self)
        self.target_groups_api = TargetGroupsApi(self)
        self.users_api = UsersApi(self)
        self.workbenches_api = WorkbenchesApi(self)

    def _init_helpers(self):
        """
        Initializes all helpers.
        """
        self.file_helper = FileHelper(self)
        self.folder_helper = FolderHelper(self)
        self.permissions_helper = PermissionsHelper(self)
        self.policy_helper = PolicyHelper(self)
        self.scan_helper = ScanHelper(self)
        self.workbench_helper = WorkbenchHelper(self)

    def _retry(f):
        """
        Decorator to retry and set the X-Tio-Retry-Count header when TenableIORetryableException is caught.
        :param f: Method to retry.
        :return: A decorated method that implicitly retry the original method upon \
        TenableIORetryableException is caught.
        """
        def wrapper(*args, **kwargs):
            total_retries = int(TenableIOClient._TOTAL_RETRIES)
            count = 0
            sleep_ms = 0
            if 'headers' not in kwargs or not kwargs['headers']:
                kwargs['headers'] = {}

            while count <= total_retries:
                # Set retry count header
                if count > 0:
                    kwargs['headers'].update({u'X-Tio-Retry-Count': str(count)})
                count += 1

                try:
                    return f(*args, **kwargs)
                except TenableIORetryableApiException as exception:
                    if count > total_retries:
                        raise TenableIOApiException(exception.response)
                    sleep_ms += count * int(TenableIOClient._RETRY_SLEEP_MILLISECONDS)
                    sleep(sleep_ms / 1000.0)
                    logging.warn(u'RETRY(%d/%d)AFTER(%dms):%s' %
                                 (count, total_retries, sleep_ms, format_request(exception.response)))
        return wrapper

    def _error_handler(f):
        """
        Decorator to handle response error.
        :param f: Response returning method.
        :return: A Response returning method that raises TenableIOException for error in response.
        """
        def wrapper(*args, **kwargs):
            response = f(*args, **kwargs)
            if response.status_code in TenableIOClient._RETRY_STATUS_CODES:
                raise TenableIORetryableApiException(response)
            if not 200 <= response.status_code <= 299:
                raise TenableIOApiException(response)
            return response
        return wrapper

    @staticmethod
    def impersonate(username):
        return TenableIOClient(impersonate=username)

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

    @classmethod
    def _flatten_param(cls, params):
        """
        Flatten the query params to be compatible with the API.
        :param params: The params object to process.
        :return: Nested dict/list values are flatten into single level dict.
        """
        flatten = params
        if type(params) in [dict, list]:
            flatten = {}
            for k, v in (params.items() if type(params) is dict else enumerate(params)):
                f = cls._flatten_param(v)
                if type(f) is dict:
                    for kk, vv in f.items():
                        flatten[u'%s.%s' % (k, kk)] = vv
                else:
                    flatten[k] = v
        return flatten

    def _request(self, method, uri, path_params=None, flatten_params=True, **kwargs):
        if path_params:
            # Ensure path param is encoded.
            path_params = {key: quote(str(value), safe=u'') for key, value in path_params.items()}
            uri %= path_params

        # Custom nested object flattening
        if flatten_params and 'params' in kwargs:
            kwargs['params'] = self._flatten_param(kwargs['params'])

        full_uri = self._endpoint + uri

        response = self._session.request(method, full_uri, **kwargs)
        log_message = format_request(response)

        logging.info(log_message)
        if not 200 <= response.status_code <= 299:
            logging.error(log_message)

        return response

    # Delayed qualifying decorator as staticmethod. This is a workaround to error raised from using a decorator
    # decorated by @staticmethod.
    _error_handler = staticmethod(_error_handler)
