from tenable_io.api.base import BaseApi
from tenable_io.api.models import ServerProperties, ServerStatus


class ServerApi(BaseApi):

    def properties(self):
        """Return the server version and other properties.

        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.ServerStatus`.
        """
        response = self._client.get('server/properties')
        return ServerProperties.from_json(response.text)

    def status(self):
        """Return server status.

        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.ServerStatus`.
        """
        response = self._client.get('server/status')
        return ServerStatus.from_json(response.text)
