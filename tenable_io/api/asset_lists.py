from tenable_io.api.base import BaseApi, BaseRequest
from tenable_io.api.models import AssetList, AssetListList


class AssetListsApi(BaseApi):

    def create(self, asset_list_create):
        """Create a new asset list.

        :param asset_list_create: An instance of :class:`AssetListCreateRequest`.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.AssetList`.
        """
        response = self._client.post('asset-lists', asset_list_create)
        return AssetList.from_json(response.text)

    def delete(self, asset_list_id):
        """Delete an asset list.

        :param asset_list_id: The asset ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: True if successful
        """
        self._client.delete('asset-lists/%(list_id)s', {'list_id': asset_list_id})
        return True

    def details(self, asset_list_id):
        """Return details of the asset list.

        :param asset_list_id: The asset ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.AssetList`.
        """
        response = self._client.get('asset-lists/%(list_id)s', {'list_id': asset_list_id})
        return AssetList.from_json(response.text)

    def edit(self, asset_list_edit, asset_list_id):
        """Modify an asset list.

        :param asset_list_edit: An instance of :class:`AssetListCreateRequest`
        :param asset_list_id: The asset list ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.AssetList`
        """
        response = self._client.put('asset-lists/%(list_id)s', asset_list_edit, {'list_id': asset_list_id})
        return AssetList.from_json(response.text)

    def list(self):
        """Return the current asset lists.

        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.AssetListList`
        """
        response = self._client.get('asset-lists')
        return AssetListList.from_json(response.text)


class AssetListCreateRequest(BaseRequest):

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


class AssetListEditRequest(AssetListCreateRequest):
    pass
