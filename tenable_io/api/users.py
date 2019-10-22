from json import loads

from tenable_io.api.base import BaseApi, BaseRequest
from tenable_io.api.models import User, UserKeys, UserList, UserAuthorizations


class UsersApi(BaseApi):

    def get(self, user_id):
        response = self._client.get('users/%(user_id)s', {'user_id': user_id})
        return User.from_json(response.text)

    def list(self):
        """Return the user list.

        :return: An instance of :class:`tenable_io.api.models.UserList`.
        """
        response = self._client.get('users')
        return UserList.from_json(response.text)

    def impersonate(self, user_id):
        response = self._client.post('users/%(user_id)s/impersonate', path_params={'user_id': user_id})
        return loads(response.text)

    def create(self, user_create):
        """Create a new user.

        :param user_create: An instance of :class:`UserCreateRequest`.
        :raise TenableIOApiException:  When API error is encountered.
        :return: The ID of the created user.
        """
        response = self._client.post('users', user_create)
        return loads(response.text).get('id')

    def edit(self, user_id, user_edit):
        """Edit an existing user.

        :param user_id: The user ID.
        :param user_edit: An instance of :class:`UserEditRequest`.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.User`.
        """
        response = self._client.put('users/%(user_id)s', user_edit, {'user_id': user_id})
        return User.from_json(response.text)

    def delete(self, user_id):
        """Delete a user.

        :param user_id: The user ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.delete('users/%(user_id)s', {'user_id': user_id})
        return True

    def password(self, user_id, password):
        """Change the password for the given user.

        :param user_id: The user ID.
        :param password: Current password for the user.
        :raise TenableIOApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.put('users/%(user_id)s/chpasswd', {'password': password}, {'user_id': user_id})
        return True

    def details(self, user_id):
        """Return details for the given user.

        :param user_id: The user ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.User`
        """
        response = self._client.get('users/%(user_id)s', {'user_id': user_id})
        return User.from_json(response.text)

    def keys(self, user_id):
        """Generate the API Keys for the given user.

        :param user_id: The user ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.UserKeys`
        """
        response = self._client.put('users/%(user_id)s/keys', path_params={'user_id': user_id})
        return UserKeys.from_json(response.text)

    def enabled(self, user_id, enabled):
        """Enable or disable an user.

        :param user_id: The user ID.
        :param enabled: True to enable. False to Disable.
        :raise TenableIOApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.put('users/%(user_id)s/enabled', {'enabled': enabled}, {'user_id': user_id})
        return True

    def authorizations(self, user_id):
        """Returns authorizations for a specified user.

        :param user_id: The user ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.UserAuthorizations`
        """
        response = self._client.get('users/%(user_id)s/authorizations', {'user_id': user_id})
        return UserAuthorizations.from_json(response.text)

    def update_authorizations(self, user_id, authorizations_update):
        """Updates a user's authorizations.

        :param user_id: The user ID.
        :param authorizations_update: An instance of :class:`UserAuthorizationsRequest`.
        :raise TenableIOApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.put('users/%(user_id)s/authorizations', authorizations_update, {'user_id': user_id})
        return True


class UserCreateRequest(BaseRequest):

    def __init__(
            self,
            username=None,
            password=None,
            permissions=None,
            name=None,
            email=None,
            type=None
    ):
        self.username = username
        self.password = password
        self.permissions = permissions
        self.name = name
        self.email = email
        self.type = type


class UserEditRequest(BaseRequest):

    def __init__(
            self,
            permissions=None,
            name=None,
            email=None
    ):
        self.permissions = permissions
        self.name = name
        self.email = email

class UserAuthorizationsRequest(BaseRequest):

    def __init__(
            self,
            api_permitted=None,
            password_permitted=None,
            saml_permitted=None
    ):
        self.api_permitted = api_permitted
        self.password_permitted = password_permitted
        self.saml_permitted = saml_permitted

