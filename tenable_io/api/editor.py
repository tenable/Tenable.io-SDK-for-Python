from tenable_io.api.base import BaseApi
from tenable_io.api.models import TemplateList


class EditorApi(BaseApi):

    def list(self, type):
        """Returns the template list.

        :param type: The type of template (scan or policy).
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.TemplateList`.
        """
        response = self._client.get('editor/%(type)s/templates', path_params={'type': type})
        return TemplateList.from_json(response.text)
