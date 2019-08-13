import pytest

from tenable_io.api.models import ImportAssetJob, ImportAssetJobs


@pytest.mark.vcr()
def test_import_assets(import_asset):
    assert import_asset, u'The `assets` method returns a valid export UUID'


@pytest.mark.vcr()
def test_import_asset_jobs(client):
    import_asset_jobs = client.import_api.asset_jobs()
    assert isinstance(import_asset_jobs, ImportAssetJobs), u'The `asset_jobs` method did not return type `ImportAssetJobs`.'


@pytest.mark.vcr()
def test_import_asset_job(client, import_asset):
    job_uuid = import_asset
    job_details = client.import_api.asset_job(job_uuid)
    assert isinstance(job_details, ImportAssetJob), u'Should be a list of `ImportAssetJob` objects.'
    assert job_details.job_id == job_uuid, u'Job uuid should match results.'
    assert job_details.batches == 1, u'Expected a single batch to be created'
