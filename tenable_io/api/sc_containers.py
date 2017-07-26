import json

from tenable_io.api.base import BaseApi
from tenable_io.api.models import ScContainer


class ScContainersApi(BaseApi):

    def delete(self, repository_name, sha256):
        """Delete a container image.

        :param repository_name: The registry/path of the image. For example, if you have a repository named unix and an
            image named alpine, you would type unix/alpine.
        :param sha256: SHA256 checksum of the container image.
        :raise TenableIOApiException:  When API error is encountered.
        :return: True if successful.
        """
        # Constructing the repository_name part of the URI first because the service does not expect this portion of the
        # URI encoded, i.e. retain any slashes in repository_name.
        uri = 'container-security/api/v1/container/%(repository_name)s/manifests/%%(sha256)s' % \
              {'repository_name': repository_name}
        response = self._client.delete(uri, path_params={'sha256': sha256})
        return json.loads(response.text)

    def list(self):
        """List container images stored.

        :raise TenableIOApiException:  When API error is encountered.
        :return: A list of :class:`tenable_io.api.models.ScContainer`.
        """
        response = self._client.get('container-security/api/v1/container/list')
        return ScContainer.from_json_list(response.text)
