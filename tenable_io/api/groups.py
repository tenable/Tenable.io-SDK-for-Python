from tenable_io.api.base import BaseApi
from tenable_io.api.models import Group, GroupList, UserList


class GroupsApi(BaseApi):

    def add_user(self, group_id, user_id):
        """Add a user to the group.

        :param group_id: The group ID.
        :param user_id: The user ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.post('groups/%(group_id)s/users/%(user_id)s', {},
                          path_params={'group_id': group_id, 'user_id': user_id})
        return True

    def create(self, name):
        """Create a group.

        :param name: The group name.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.Group`.
        """
        response = self._client.post('groups', {'name': name})
        return Group.from_json(response.text)

    def delete(self, group_id):
        """Delete a group.

        :param group_id: The group ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.delete('groups/%(group_id)s', {'group_id': group_id})
        return True

    def delete_user(self, group_id, user_id):
        """Delete a user from the group.

        :param group_id: The group ID.
        :param user_id: The user ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.delete('groups/%(group_id)s/users/%(user_id)s', {'group_id': group_id, 'user_id': user_id})
        return True

    def edit(self, group_id, name):
        """Edit a group.

        :param group_id: The group ID.
        :param name: The group name.
        :return: True if successful.
        """
        self._client.put('groups/%(group_id)s', {'name': name}, {'group_id': group_id})
        return True

    def list(self):
        """Return the group list.

        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.Grouplist`.
        """
        response = self._client.get('groups')
        return GroupList.from_json(response.text)

    def list_users(self, group_id):
        """Return the user list in the group.

        :param group_id: The group ID.
        :return: An instance of :class:`tenable_io.api.models.UserList`.
        """
        response = self._client.get('groups/%(group_id)s/users', {'group_id': group_id})
        return UserList.from_json(response.text)
