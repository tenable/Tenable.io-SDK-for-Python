from tenable_io.api.base import BaseApi
from tenable_io.api.models import ScTestJob


class ScTestJobsApi(BaseApi):

    def status(self, job_id):
        """Get the status of a test.

        :param job_id: The job ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.ScTestJob`.
        """
        response = self._client.get('container-security/api/v1/jobs/status', params={'job_id': job_id})
        return ScTestJob.from_json(response.text)

    def by_image(self, image_id):
        """Get the status of a test by Docker image ID.

        :param image_id: The Docker image ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.ScTestJob`.
        """
        response = self._client.get('container-security/api/v1/jobs/image_status', params={'image_id': image_id})
        return ScTestJob.from_json(response.text)

    def by_image_digest(self, sha256):
        """Get the status of a test by SHA256 checksum.

        :param sha256: SHA256 checksum of the container image.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.ScTestJob`.
        """
        response = self._client.get('container-security/api/v1/jobs/image_status_digest',
                                    params={'image_digest': sha256})
        return ScTestJob.from_json(response.text)

    def list(self):
        """Get active and recent jobs.

        :raise TenableIOApiException:  When API error is encountered.
        :return: A list of :class:`tenable_io.api.models.ScTestJob`.
        """
        response = self._client.get('container-security/api/v1/jobs/list')
        return ScTestJob.from_json_list(response.text)
