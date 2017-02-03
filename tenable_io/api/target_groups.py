from tenable_io.api.base import BaseApi, BaseRequest
from tenable_io.api.models import TargetGroup, TargetGroupList


class TargetGroupsApi(BaseApi):

    def create(self, target_group_create):
        """Create a new target group.

        :param target_group_create: An instance of :class:`TargetGroupCreateRequest`.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.TargetGroup`.
        """
        response = self._client.post('target-groups', target_group_create)
        return TargetGroup.from_json(response.text)

    def delete(self, group_id):
        """Delete a target group.

        :param group_id: The group ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: True if successful
        """
        self._client.delete('target-groups/%(group_id)s', {'group_id': group_id})
        return True

    def details(self, group_id):
        """Return details of the target group.

        :param group_id: The group ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.TargetGroup`.
        """
        response = self._client.get('target-groups/%(group_id)s', {'group_id': group_id})
        return TargetGroup.from_json(response.text)

    def edit(self, target_group_edit, group_id):
        """Modify a target group.

        :param target_group_edit: An instance of :class:`TargetGroupCreateRequest`
        :param group_id: The group ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.TargetGroup`
        """
        response = self._client.put('target-groups/%(group_id)s', target_group_edit, {'group_id': group_id})
        return TargetGroup.from_json(response.text)

    def list(self):
        """Return the current target groups.

        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.TargetGroupList`
        """
        response = self._client.get('target-groups')
        return TargetGroupList.from_json(response.text)


class TargetGroupCreateRequest(BaseRequest):

    def __init__(
            self,
            name=None,
            members=None,
            type=None,
            acls=None
    ):
        self.name = name
        self.members = members
        self.type = type
        self.acls = acls


class TargetListEditRequest(TargetGroupCreateRequest):
    pass
