import os

from tests.base import BaseTest

from tenable_io.api.models import AssetList, VulnerabilityList
from tenable_io.api.workbenches import WorkbenchesApi
from tenable_io.exceptions import TenableIOErrorCode, TenableIOApiException


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

    def test_export(self, app, client):
        file_id = client.workbenches_api.export_request(
            WorkbenchesApi.FORMAT_NESSUS,
            WorkbenchesApi.REPORT_VULNERABILITIES,
            WorkbenchesApi.CHAPTER_VULN_BY_ASSET,
        )
        assert file_id, u'The `export_request` method returns a valid file ID.'

        export_status = self.wait_until(lambda: client.workbenches_api.export_status(file_id),
                                        lambda status: status == WorkbenchesApi.STATUS_EXPORT_READY)

        assert export_status == WorkbenchesApi.STATUS_EXPORT_READY, u'Workbench export is ready.'

        iter_content = client.workbenches_api.export_download(file_id, False)
        download_path = app.session_file_output('test_workbench_export')

        assert not os.path.isfile(download_path), u'Workbench report does not yet exist.'

        with open(download_path, 'wb') as fd:
            for chunk in iter_content:
                fd.write(chunk)
        assert os.path.isfile(download_path), u'Workbench report is downloaded.'
        assert os.path.getsize(download_path) > 0, u'Workbench report is not empty.'

        os.remove(download_path)
