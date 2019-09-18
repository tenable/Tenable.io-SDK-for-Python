from json import loads

from tenable_io.api.base import BaseApi
from tenable_io.api.base import BaseRequest
from tenable_io.api.models import AssetTagAssignmentList, TagCategory, TagCategoryList, TagValue, TagValueList, TagValueFilters


class TagsApi(BaseApi):

    def categories(self):
        """Return the tag category list.

        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.TagCategoryList`.
        """
        response = self._client.get('tags/categories')
        return TagCategoryList.from_json(response.text)

    def create_category(self, tag_category_request):
        """Create a tag category.

        :param tag_category_request: An instance of :class:`TagCategoryRequest`.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.TagCategory`.
        """
        response = self._client.post('tags/categories', tag_category_request)
        return TagCategory.from_json(response.text)

    def delete_category(self, uuid):
        """Delete a tag category.

        :param uuid: The uuid of the tag category to delete.
        :raise TenableIOApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.delete('tags/categories/%(uuid)s', path_params={'uuid': uuid})
        return True

    def category(self, uuid):
        """Find a tag category by uuid.

        :param uuid: The uuid of the tag category to retreive.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.TagCategory`.
        """
        response = self._client.get('tags/categories/%(uuid)s', path_params={'uuid': uuid})
        return TagCategory.from_json(response.text)

    def edit_category(self, uuid, tag_category_request):
        """Edit existing category.

        :param uuid: The uuid of the category to be edited.
        :param tag_category_request: An instance of :class:`TagCategoryRequest`.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.TagCategory`.
        """
        response = self._client.put('tags/categories/%(uuid)s',
                                    payload=tag_category_request,
                                    path_params={'uuid': uuid})
        return TagCategory.from_json(response.text)

    def category_values(self, uuid):
        """Return the values for specified category

        :param uuid: The uuid of the category for which to retreive values.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.TagValueList`.
        """
        response = self._client.get('tags/categories/%(uuid)s/values', path_params={'uuid': uuid})
        return TagValueList.from_json(response.text)

    def category_value(self, category_uuid, value_uuid):
        """Return specific value for specified category

        :param category_uuid: The uuid of the category for which to retreive value.
        :param value_uuid: The uuid of the value to be retreived
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.TagValue`.
        """
        response = self._client.get('tags/categories/%(category_uuid)s/values/%(value_uuid)s',
                                    path_params={'category_uuid': category_uuid, 'value_uuid': value_uuid})
        return TagValue.from_json(response.text)

    def category_counts(self, uuid):
        """Return category assignment counts

        :param uuid: The uuid of the category for which to retreive assignment count.
        :raise TenableIOApiException:  When API error is encountered.
        :return: The category assignment count or None if it contains no assignment
        """
        response = self._client.get('tags/categories/%(uuid)s/counts', path_params={'uuid': uuid})
        return loads(response.text).get('counts', {}).get('asset')

    def values(self):
        """Return the tag value list.

        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.TagValueList`.
        """
        response = self._client.get('tags/values')
        return TagValueList.from_json(response.text)

    def create_value(self, value_request):
        """Create a new tag value

        :param value_request: An instance of :class: `TagValueRequest
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.TagValue`.
        """
        response = self._client.post('tags/values', value_request)
        return TagValue.from_json(response.text)

    def delete_value(self, uuid):
        """Delete a tag value.

        :param uuid: The uuid of the tag value to delete.
        :raise TenableIOApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.delete('tags/values/%(uuid)s', path_params={'uuid': uuid})
        return True

    def value(self, uuid):
        """Find a tag value by uuid.

        :param uuid: The uuid of the tag value to retreive.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.TagValue`.
        """
        response = self._client.get('tags/values/%(uuid)s', path_params={'uuid': uuid})
        return TagValue.from_json(response.text)

    def edit_value(self, uuid, tag_value_request):
        """Edit existing tag value.

        :param uuid: The uuid of the value to be edited.
        :param tag_value_request: An instance of :class:`TagValueRequest`.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.TagValue`.
        """
        response = self._client.put('tags/values/%(uuid)s', payload=tag_value_request, path_params={'uuid': uuid})
        return TagValue.from_json(response.text)

    def value_counts(self, uuid):
        """Return value assignment counts

        :param uuid: The uuid of the value for which to retreive assignment count.
        :raise TenableIOApiException:  When API error is encountered.
        :return: The value assignment count or None if it contains no assignments
        """
        response = self._client.get('tags/values/%(uuid)s/counts', path_params={'uuid': uuid})
        return loads(response.text).get('counts', {}).get('asset')

    def value_delete_requests(self, values):
        """Bulk delete values

        :param values: List of value identifiers to delete
        :raise TenableIOApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.post('tags/values/delete-requests', {'values': values})
        return True

    def asset_tag_assignments(self, asset_id):
        """Retreive asset tag assignments

        :param asset_id: The asset id for which to retreive assigned tags
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.AssetTagAssignmentList`.
        """
        response = self._client.get('tags/assets/%(asset_id)s/assignments', path_params={'asset_id': asset_id})
        return AssetTagAssignmentList.from_json(response.text)

    def edit_asset_tag_assignments(self, assignments_request):
        """Add or remove asset tag assignments

        :param assignments_request: An instance of :class:`AssetAssignmentsRequest`.
        :raise TenableIOApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.post('tags/assets/assignments', assignments_request)
        return True


class TagCategoryRequest(BaseRequest):

    def __init__(
            self,
            name,
            description=None,
    ):
        """Request for TagsApi.create_category and TagsApi.edit_category.

        :param name: The name of the tag category.
        :type name: string
        :param description: The description of the tag category.
        :type description: string
        """
        self.name = name
        self.description = description


class TagValueRequest(BaseRequest):

    def __init__(
            self,
            value,
            category_uuid=None,
            category_name=None,
            category_description=None,
            description=None,
            filters=None
    ):
        """Request for TagsApi.create_value and TagsApi.edit_value.

        :param category_uuid: The uuid of category to add value to
        :type category_uuid: string
        :param category_name: The category name
        :type category_name: string
        :param category_description: The category description
        :type category_description: string
        :param value: The value to be added
        :type value: string
        :param description: The description of the tag value.
        :type description: string
        :param filters: Optional filters to create a dynamic tag
        :type filters: TagValueFilters
        """
        self.category_uuid = category_uuid
        self.category_name = category_name
        self.category_description = category_description
        self.value = value
        self.description = description
        if filters is not None:
            assert filters.operator in [
                TagValueFilters.OPERATOR_AND,
                TagValueFilters.OPERATOR_OR
            ]
            self.filters = filters.as_payload()


class AssetAssignmentsRequest(BaseRequest):

    def __init__(
            self,
            action=None,
            assets=None,
            tags=None
    ):
        """Request for TagsApi.edit_asset_tag_assignments.

        :param action: The action to be performed. Can have a value of **add** or **remove**.
        :type action: string
        :param assets: The list of asset identifiers to be updated
        :type assets: list
        :param tags: The list of tag values to update assets with
        :type tags: list
        """
        self.action = action
        self.assets = assets
        self.tags = tags
