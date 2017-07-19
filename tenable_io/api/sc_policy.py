from json import loads

from tenable_io.api.base import BaseApi


class ScPolicyApi(BaseApi):

    def compliance(self, image_id):
        """Get policy compliance status of an image.

        :param image_id: The Docker image ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: The policy status.
        """
        response = self._client.get('container-security/api/v1/policycompliance', params={'image_id': image_id})
        return loads(response.text)
