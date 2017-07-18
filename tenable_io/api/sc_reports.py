from tenable_io.api.base import BaseApi
from tenable_io.api.models import ScReport


class ScReportsApi(BaseApi):

    def show(self, container_id):
        """Get JSON format report using container ID.

        :param container_id: The ID of the container image.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class`tenable_io.api.models.ScReport`.
        """
        response = self._client.get('container-security/api/v1/reports/show', params={'container_id': container_id})
        return ScReport.from_json(response.text)

    def by_image(self, image_id):
        """Get JSON format report using docker ID.

        :param image_id: The ID of the docker image.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class`tenable_io.api.models.ScReport`.
        """
        response = self._client.get('container-security/api/v1/reports/by_image', params={'image_id': image_id})
        return ScReport.from_json(response.text)

    def by_image_digest(self, sha256):
        """Get JSON format report using SHA256.

        :param sha256: SHA256 checksum of the container image.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class`tenable_io.api.models.ScReport`.
        """
        response = self._client.get('container-security/api/v1/reports/by_image_digest',
                                    params={'image_digest': sha256})
        return ScReport.from_json(response.text)

    def nessus_show(self, id):
        """Get Nessus V2 format report using container ID.

        :param id: The ID of the container image.
        :raise TenableIOApiException:  When API error is encountered.
        :return: A Nessus V2 format report in XML.
        """
        response = self._client.get('container-security/api/v1/reports/nessus/show', params={'id': id})
        return response.text
