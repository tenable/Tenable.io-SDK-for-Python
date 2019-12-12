from json import loads

from tenable_io.api.base import BaseApi, BaseRequest
from tenable_io.api.models import CredentialList, CredentialDetails, CredentialPermission, CredentialPrimitiveType


class CredentialsApi(BaseApi):

    def list(self, f=None, ft='and', limit=None, offset=0, sort=None, referrer_owner_uuid=None):
        """Return a list of Managed Credentials.

        :param f: A list of :class:`tenable_io.api.models.CredentialFilter` instances.
        :param ft: The action to apply if multiple 'f' parameters are provided. Supported values are **and** and **or**.
        :param limit: The maximum number of records to be retrieved.
        :param offset: The offset from request.
        :param sort: A list of fields on which the results are sorted.
        :param referrer_owner_uuid: The UUID of a scan owner. This parameter limits the returned data to managed
               credentials assigned to scans owned by the specified user..
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.CredentialList`.
        """
        fgen = (i.field + ':' + i.operator + ':' + i.value for i in f) if f is not None else None
        response = self._client.get('credentials',
                                    params={'f': '&'.join(fgen) if fgen is not None else None,
                                            'ft': ft,
                                            'limit': limit, 'offset': offset,
                                            'sort': ','.join(sort) if sort is not None else None,
                                            'referrer_owner_uuid': referrer_owner_uuid
                                            if referrer_owner_uuid is not None else None})
        return CredentialList.from_json(response.text)


    def create(self, credential_request):
        """Create a new Managed Credential.

        :param credential_request: An instance of :class:`CredentialRequest`.
        :raise TenableIOApiException:  When API error is encountered.
        :return: uuid of the new Managed Credential.
        """
        response = self._client.post('credentials', credential_request)
        return loads(response.text).get('uuid')


    def details(self, uuid):
        """Returns details for a specific access group

        :param uuid: The uuid of the Managed Credential.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.CredentialDetails`.
        """
        response = self._client.get('credentials/%(uuid)s', path_params={'uuid': uuid})
        # We manually add the uuid back to the response object to it can be referenced later more easily
        credential_details = loads(response.text)
        credential_details['uuid'] = uuid
        return CredentialDetails.from_dict(credential_details)


    def update(self, uuid, credential_request):
        """Modifies an access group. This method overwrites the existing data.

        :param uuid: The uuid of the Managed Credential to be updated.
        :param credential_request: An instance of :class:`CredentialRequest`.
        :raise TenableIOApiException:  When API error is encountered.
        :return: A boolean indicating that the Managed Credential was updated successfully.
        """
        response = self._client.put('credentials/%(uuid)s', payload=credential_request, path_params={'uuid': uuid})
        return loads(response.text).get("updated")


    def delete(self, uuid):
        """Delete a Managed Credential.

        :param uuid: The uuid of the Managed Credential to delete.
        :raise TenableIOApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.delete('credentials/%(uuid)s', path_params={'uuid': uuid})
        return True


    def types(self):
        """Lists all credential types supported for managed credentials in Tenable.io.

        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.CredentialPrimitiveType`.
        """
        response = self._client.get('credentials/types')
        return CredentialPrimitiveType.from_json(response.text)


class CredentialRequest(BaseRequest):

    def __init__(
            self,
            name=None,
            description=None,
            type_=None,
            settings=None,
            permissions=None
    ):
        """Request for CredentialsApi.create and CredentialsApi.update.

        :param name: The name of the managed credential. This name must be unique within your Tenable.io instance.
        :type name: str
        :param description: The description of the managed credential object.
        :type description: str
        :param type_: The type of credential object. For a list of supported credential types, use the
            :func:`~tenable_io.CredentialsApi.types` method to get a list of possible types and the
            required configuration for each.
        :type type_: str
        :param settings: The configuration settings for the credential. The parameters of this object vary depending on
            the credential type. For more information, see our documentation at
            https://developer.tenable.com/docs/determine-settings-for-credential-type
        :type settings: dict
        :param permissions: A list of :class:`tenable_io.api.models.CredentialPermissions` objects to specify the
            permissions for the managed credential.
        :type permissions: list
        """
        if permissions is not None:
            for p in permissions:
                assert isinstance(p, CredentialPermission)

        self.name = name
        self.description = description
        self.type = type_
        self.settings = settings
        self.permissions = permissions

    def as_payload(self, filter_=None):
        payload = super(CredentialRequest, self).as_payload(True)
        _permissions = []
        if self.permissions is not None:
            for p in self.permissions:
                _permissions.append(p.as_payload(True))
            payload.__setitem__("permissions", _permissions)
        return payload
