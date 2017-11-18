from tenable_io.api.base import BaseApi
from tenable_io.api.models import Filters


class FiltersApi(BaseApi):

    def agents_filters(self):
        """Gets filtering, sorting, and pagination capabilities available for agent records.

        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class: `tenable_io.api.models.Filters`.
        """
        response = self._client.get('filters/scans/agents')
        return Filters.from_json(response.text)
