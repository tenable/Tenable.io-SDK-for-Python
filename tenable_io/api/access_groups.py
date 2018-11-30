from json import loads

from tenable_io.api.base import BaseApi
from tenable_io.api.base import BaseRequest
from tenable_io.api.models import AccessGroup, AccessGroupList, AssetRule, AssetRuleFilter, AssetRulePrincipal, Filters


class AccessGroupsApi(BaseApi):

    def list(self, f=None, ft='and', w=None, wf=None, limit=None, offset=0, sort=None):
        """Return the access groups without associated rules.

        :param f: A list of :class:`tenable_io.api.models.AssetFilter` instances.
        :param ft: The action to apply if multiple 'f' parameters are provided. Supported values are **and** and **or**.
        :param w: The search value to be applied across wildcard fields specified with the 'wf' parameter.
        :param wf: The list of fields where the search values specified in the 'w' parameter are applied.
        :param limit: The maximum number of records to be retrieved.
        :param offset: The offset from request.
        :param sort: A list of fields on which the results are sorted.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.AccessGroupList`.
        """
        fgen = (i.field + ':' + i.operator + ':' + i.value for i in f) if f is not None else None
        response = self._client.get('access-groups',
                                    params={'f': '&'.join(fgen) if fgen is not None else None,
                                            'ft': ft, 'w': w, 'wf': ','.join(wf) if wf is not None else None,
                                            'limit': limit, 'offset': offset,
                                            'sort': ','.join(sort) if sort is not None else None})
        return AccessGroupList.from_json(response.text)

    def create(self, access_group_request):
        """Create a new access group.

        :param Access_group_request: An instance of :class:`AccessGroupRequest`.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.AccessGroup` without the rules information.
        """
        response = self._client.post('access-groups', access_group_request)
        return AccessGroup.from_json(response.text)

    def details(self, id):
        """Returns details for a specific access group

        :param id: The id of the access group
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.AccessGroup`.
        """
        response = self._client.get('access-groups/%(id)s', path_params={'id': id})
        return AccessGroup.from_json(response.text)

    def delete(self, id):
        """Delete an access group.

        :param id: The id of the access group to delete.
        :raise TenableIOApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.delete('access-groups/%(id)s', path_params={'id': id})
        return True

    def edit(self, id, access_group_request):
        """Modifies an access group. This method overwrites the existing data.

        :param id: The id of the access group to be edited.
        :param access_group_request: An instance of :class:`AccessGroupRequest`.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.AccessGroup`.
        """
        response = self._client.put('access-groups/%(id)s', payload=access_group_request, path_params={'id': id})
        return AccessGroup.from_json(response.text)

    def filters(self):
        """List available filters for access groups.

        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.Filters`.
        """
        response = self._client.get('access-groups/filters')
        return Filters.from_json(response.text)

    def rule_filters(self):
        """List available filters for asset rules.

        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.Filters`.
        """
        response = self._client.get('access-groups/rules/filters')
        return AssetRuleFilter.from_list(loads(response.text).get('rules', {}))


class AccessGroupRequest(BaseRequest):

    def __init__(
            self,
            name=None,
            all_assets=False,
            all_users=False,
            rules=None,
            principals=None
    ):
        """Request for AccessGroupsApi.create and AccessGroupsApi.edit.

        :param name: The name of the access group. Must be unique within the container, a maximum of 255 characters, and
            alphanumeric, but can include limited special characters (underscore, dash, parenthesis, brackets, colon).
            You can add a maximum of 5,000 access groups to an individual container.
        :type name: string
        :param all_assets: Specifies whether the access group is the All Assets group or a user-defined group. A create
            request with this parameter set to 'true' will fail.
            Set to 'true' to edit membership in the All Assets access group. In which case, any rules
            are ignored, but existing principals are overwritten based on the all_users and principals parameters.
            Set to 'false' to edit a user-defined access group. The existing rules are overwritten with the new rules,
            and existing principals are overwritten based on the all_users and principals parameters.
        :type all_assets: boolean
        :param all_users: Specifies whether assets in the access group can be viewed by all or only some users.
            Default is 'False'. If 'true', all users in your organization have Can View access to the
            assets defined in the rules parameter and any principal parameters is ignored.
            If 'false', only specified users have Can View access to the assets defined in the rules parameter.
            You define which users or user groups have access in the principals parameter of the request.
        :type all_users: boolean
        :param rules: An array of asset rules. Tenable.io uses these rules to assign assets to the access group.
            You can only add rules to access groups if the all_assets parameter is set to 'false'.
        :type rules: list
        :param principals: A list of principals. Each representing a user or user group assigned to the access group.
            Data in this array is handled based on the all_users parameter. If all_users is 'true',
            any principal data is ignored and you can omit this parameter.
            If all_users is 'false', the principal data is added to the access group.
        :type principals: list
        """
        for r in rules:
            assert isinstance(r, AssetRule)

        self.name = name
        self.all_assets = all_assets
        self.all_users = all_users
        self.rules = rules
        self.principals = principals

    def as_payload(self, filter_=None):
        payload = super(AccessGroupRequest, self).as_payload(True)
        rule_list = []
        for r in self.rules:
            rule_list.append(r.as_payload())
        payload.__setitem__('rules', rule_list)
        if not self.all_users and self.principals:
            principal_list = []
            for p in self.principals:
                assert isinstance(p, AssetRulePrincipal)
                principal_list.append(p.as_payload())
            payload.__setitem__('principals', principal_list)
        return payload
