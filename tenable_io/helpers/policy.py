from tenable_io.api.models import Template
from tenable_io.api.policies import PolicyCreateRequest, PolicyImportRequest, PolicySettings
from tenable_io.exceptions import TenableIOException


class PolicyHelper(object):

    def __init__(self, client):
        self._client = client

    def create(self, name, template):
        """Create a policy.

        :param name: The name of the policy.
        :param template: The name or title of the template, or an instance of Template.
        :return: PolicyRef referenced by id if exists.
        """
        t = template

        if not isinstance(t, Template):
            t = self.template(name=template)

        if not t:
            t = self.template(title=template)

        if not t:
            raise TenableIOException(u'Template with name or title as "%s" not found.' % template)

        policy_id = self._client.policies_api.create(
            PolicyCreateRequest(
                t.uuid,
                PolicySettings(name=name)
            )
        )
        return PolicyRef(self._client, policy_id)

    def import_policy(self, path):
        """Upload and import the policy file.

        :param path: Path of the policy file.
        :return: PolicyRef referenced by id if exists.
        """
        uploaded_file_name = self._client.file_helper.upload(path)

        policy_id = self._client.policies_api.import_policy(
            PolicyImportRequest(uploaded_file_name)
        )

        return PolicyRef(self._client, policy_id)

    def template(self, name=None, title=None):
        """Get template by name or title. The 'title' argument is ignored if 'name is passed.

        :param name: The name of the template.
        :param title: The title of the template.
        :return: An instance of Template if exists, otherwise None.
        """
        template = None

        if name:
            template_list = self._client.editor_api.list('policy')
            for t in template_list.templates:
                if t.name == name:
                    template = t
                    break

        elif title:
            template_list = self._client.editor_api.list('policy')
            for t in template_list.templates:
                if t.title == title:
                    template = t
                    break

        return template


class PolicyRef(object):

    def __init__(self, client, id):
        self._client = client
        self.id = id

    def copy(self):
        """Create a copy of the policy.

        :return: An instance of PolicyRef that references the newly copied policy.
        """
        policy_id = self._client.policies_api.copy(self.id)
        return PolicyRef(self._client, policy_id)

    def delete(self):
        """Delete the policy.

        :return: The same PolicyRef Instance.
        """
        self._client.policies_api.delete(self.id)
        return self

    def details(self):
        """Get the policy detail.

        :return: An instance of :class:`tenable_io.api.models.PolicyDetails`.
        """
        return self._client.policies_api.details(self.id)

    def download(self, path, file_open_mode='wb'):
        """Download a policy file.

        :param path: The file path to save the file.
        :param file_open_mode: The open mode to the file output. Default to 'wb'.
        :return: The same PolicyRef instance.
        """
        iter_content = self._client.policies_api.export(self.id)
        with open(path, file_open_mode) as fd:
            for chunk in iter_content:
                fd.write(chunk)
        return self

    def name(self):
        """Get the name of the policy.

        :return:  The name.
        """
        return self.details().settings.name
