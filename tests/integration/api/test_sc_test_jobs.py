import pytest

from tenable_io.api.models import ScTestJob

from tests.integration.api.utils.utils import upload_image


@pytest.mark.skip('Deprecated v1 API')
@pytest.mark.vcr()
def test_sc_test_jobs_status(client):
    _ = upload_image('test_sc_test_jobs_status', 'test_sc_test_jobs_status')
    jobs = client.sc_test_jobs_api.list()
    assert len(jobs) > 0, u'At least one job exists.'
    test_job = client.sc_test_jobs_api.status(jobs[0].job_id)
    assert isinstance(test_job, ScTestJob), u'The method returns type.'


@pytest.mark.vcr()
def test_sc_test_jobs_by_image(client):
    image = upload_image('test_sc_test_jobs_by_image', 'test_sc_test_jobs_by_image')
    job = client.sc_test_jobs_api.by_image(image['id'])
    assert isinstance(job, ScTestJob), u'The method returns type.'


@pytest.mark.vcr()
def test_sc_test_jobs_by_image_digest(client):
    image = upload_image('test_sc_test_jobs_by_image_digest', 'test_sc_test_jobs_by_image_digest')
    job = client.sc_test_jobs_api.by_image_digest(image['digest'])
    assert isinstance(job, ScTestJob), u'The method returns type.'


@pytest.mark.vcr()
def test_sc_test_jobs_list(client):
    _ = upload_image('test_sc_test_jobs_list', 'test_sc_test_jobs_list')
    jobs = client.sc_test_jobs_api.list()
    assert len(jobs) > 0, u'At least one job exists.'
    assert isinstance(jobs[0], ScTestJob), u'The method returns job list.'
