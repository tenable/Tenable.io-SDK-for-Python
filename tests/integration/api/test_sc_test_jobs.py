from tests.base import BaseTest

from tenable_io.api.models import ScTestJob


class TestScTestJobsApi(BaseTest):

    def test_status(self, client, image):
        jobs = client.sc_test_jobs_api.list()
        assert len(jobs) > 0, u'At least one job exists.'
        test_job = client.sc_test_jobs_api.status(jobs[0].job_id)
        assert isinstance(test_job, ScTestJob), u'The method returns type.'

    def test_by_image(self, client, image):
        job = client.sc_test_jobs_api.by_image(image['id'])
        assert isinstance(job, ScTestJob), u'The method returns type.'

    def test_by_image_digest(self, client, image):
        job = client.sc_test_jobs_api.by_image_digest(image['digest'])
        assert isinstance(job, ScTestJob), u'The method returns type.'

    def test_list(self, client, image):
        jobs = client.sc_test_jobs_api.list()
        assert len(jobs) > 0, u'At least one job exists.'
        assert isinstance(jobs[0], ScTestJob), u'The method returns job list.'
