from tenable_io.api.base import BaseApi
from tenable_io.api.models import EditorConfigurationDetails, EditorPluginDetails, EditorTemplateDetails, TemplateList

SCAN = u'scan'
POLICY = u'policy'

class EditorApi(BaseApi):

    def list(self, type):
        """Returns the template list.

        :param type: The type of template (scan or policy).
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.TemplateList`.
        """
        response = self._client.get('editor/%(type)s/templates', path_params={'type': type})
        return TemplateList.from_json(response.text)


    def details(self, type, id):
        """
        Gets the configuration details for the scan or policy.
        :param type: Type of entity, must be `scan` or `policy`.
        :param id: numeric id of the object.
        :return: An instance of :class:`tenable_io.api.models.EditorConfigurationDetails`.
        """
        response = self._client.get('editor/%(type)s/%(id)s', path_params={'type': type, 'id': id})
        return EditorConfigurationDetails.from_json(response.text)


    def template_details(self, type, uuid):
        """
        Gets the configuration details for a template.
        :param type: Type of entity, must be `scan` or `policy`.
        :param uuid: UUID of the template.
        :return: An instance of :class:`tenable_io.api.models.EditorTemplateDetails`.
        """
        response = self._client.get('editor/%(type)s/templates/%(uuid)s', path_params={'type': type, 'uuid': uuid})
        return EditorTemplateDetails.from_json(response.text)


    def plugin_details(self, policy_id, family_id, plugin_id):
        """
        Gets the configuration details for a plugin.
        :param policy_id: id of the policy.
        :param family_id: id of the plugin family.
        :param plugin_id: id of the plugin.
        :return: An instance of :class:`tenable_io.api.models.EditorPluginDescription`.
        """
        response = self._client.get('editor/policy/%(policy_id)s/families/%(family_id)s/plugins/%(plugin_id)s',
                                    path_params={'policy_id': policy_id,
                                                 'family_id': family_id,
                                                 'plugin_id': plugin_id})
        return EditorPluginDetails.from_json(response.text).plugindescription
