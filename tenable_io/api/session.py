from tenable_io.api.base import BaseApi
from tenable_io.api.models import Session


class SessionApi(BaseApi):

    def get(self):
        """Return the user session data.

        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.Session`.
        """
        response = self._client.get('session')
        return Session.from_json(response.text)
