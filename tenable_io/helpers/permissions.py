from tenable_io.api.models import Permissions


class PermissionsHelper(object):

    def __init__(self, client):
        self._client = client

    def default_scan(self, access_level):
        """Generates a Permission object for the default role.

        :param access_level: The access level the default user group should be granted for a scan (0, 16, 32, 64). See `Permissions.Scan`.
        :return: A Permissions instance
        """
        return Permissions(type=Permissions.Type.DEFAULT,
                           permissions=access_level)

    def user_scan(self, user_id, access_level):
        """Generates a Permission object for the given user id with the given permissions

        :param user_id: Numeric User Id
        :param access_level: The access level the default user group should be granted for a scan (0, 16, 32, 64). See `Permissions.Scan`.
        :return: A Permissions instance
        """
        user = self._client.users_api.get(user_id)
        return Permissions(owner=user.id,
                           type=Permissions.Type.USER,
                           permissions=access_level,
                           id=user.id,
                           name=user.name)

    def as_acl(self, permissions):
        """Can be used as part of an acl.

        :param permissions: An instance of `Permissions`
        :return: dict
        """
        return permissions.as_payload()
