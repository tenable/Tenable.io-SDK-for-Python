from tests.base import BaseTest

from tenable_io.api.import_ import ImportAssetsRequest
from tenable_io.api.models import ImportAsset, ImportAssetJob, ImportAssetJobs
from tenable_io.exceptions import TenableIOErrorCode, TenableIOApiException


class TestImportApi(BaseTest):

    def test_assets(self, client):
        try:
            client.import_api.assets(ImportAssetsRequest(assets=[], source=None))
            assert False, u'TenableIOApiException should have been thrown for bad ID.'
        except TenableIOApiException as e:
            assert e.code is TenableIOErrorCode.BAD_REQUEST, u'Appropriate exception thrown.'

    def test_asset_jobs(self, client):
        import_asset_jobs = client.import_api.asset_jobs()
        assert isinstance(import_asset_jobs, ImportAssetJobs), u'List request returns type.'
        for i in import_asset_jobs.asset_import_jobs:
            assert isinstance(i, ImportAssetJob)

    def test_asset_job(self, client):
        try:
            client.import_api.asset_job('test_import_asset_job')
            assert False, u'TenableIOApiException should have been thrown for bad ID.'
        except TenableIOApiException as e:
            assert e.code in (TenableIOErrorCode.BAD_REQUEST, TenableIOErrorCode.NOT_FOUND), \
                u'Bad request for string agent_id or agent not found.'
