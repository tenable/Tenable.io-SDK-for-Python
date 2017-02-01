from tests.base import BaseTest

from tenable_io.exceptions import TenableIOErrorCode, TenableIOApiException
from tenable_io.api.models import AssetList, VulnerabilityList


class TestWorkbenchesApi(BaseTest):

    def test_assets(self, client):
        assets_list = client.workbenches_api.assets()
        assert isinstance(assets_list, AssetList), u'The method returns asset list.'

    def test_assets_vulnerabilities(self, client):
        assets_list = client.workbenches_api.assets_vulnerabilities()
        assert isinstance(assets_list, AssetList), u'The method returns asset list.'

    def test_asset_info(self, client):
        try:
            client.workbenches_api.asset_info('test_asset_info')
            assert False, u'TenableIOApiException should have been thrown for bad ID.'
        except TenableIOApiException as e:
            assert e.code is TenableIOErrorCode.BAD_REQUEST, u'Appropriate exception thrown.'

    def test_asset_vulnerabilities(self, client):
        try:
            client.workbenches_api.asset_vulnerabilities('test_asset_vulnerabilities')
            assert False, u'TenableIOApiException should have been thrown for bad ID.'
        except TenableIOApiException as e:
            assert e.code is TenableIOErrorCode.BAD_REQUEST, u'Appropriate exception thrown.'

    def test_vulnerabilities(self, client):
        vulnerabilities_list = client.workbenches_api.vulnerabilities()
        assert isinstance(vulnerabilities_list, VulnerabilityList), u'The method returns vulnerability list.'

    def test_vulnerability_output(self, client):
        try:
            client.workbenches_api.vulnerability_output('test_vulnerability_output')
            assert False, u'TenableIOApiException should have been thrown for bad ID.'
        except TenableIOApiException as e:
            assert e.code is TenableIOErrorCode.BAD_REQUEST, u'Appropriate exception thrown.'
