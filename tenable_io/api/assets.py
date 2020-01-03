from tenable_io.api.base import BaseApi, BaseRequest
from tenable_io.api.models import AssetsAssetDetails, AssetsAssetList, BulkAsset


class AssetsApi(BaseApi):

    def list(self):
        """List all the assets.

        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`AssetsAssetList`.
        """
        response = self._client.get('assets')
        return AssetsAssetList.from_json(response.text)

    def get(self, asset_id):
        """Get asset info.

        :param asset_id: The asset ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`AssetsAssetDetails`.
        """
        response = self._client.get('assets/%(asset_id)s', path_params={'asset_id': asset_id})
        return AssetsAssetDetails.from_json(response.text)

    def bulk_move(self, bulk_move):
        """Bulk move assets to a different Network.

        Note: This API required Admin [64] permissions.

        :param bulk_move: An instance of :class:`BulkMoveRequest`.
        :return: int - The total number of assets affected.
        """
        response = self._client.post('api/v2/assets/bulk-jobs/move-to-network',
                                     bulk_move)
        return BulkAsset.from_json(response.text).response['data']['asset_count']

    def bulk_delete(self, bulk_delete):
        """Bulk delete assets using a filter query.

        Note: This API required Admin [64] permissions.

        :param bulk_delete: An instance of :class:`BulkDeleteRequest`.
        :return: int - The total number of assets affected.
        """
        response = self._client.post('api/v2/assets/bulk-jobs/delete',
                                     bulk_delete)
        return BulkAsset.from_json(response.text).response['data']['asset_count']


class BulkMoveRequest(BaseRequest):

    def __init__(
            self,
            source=None,
            destination=None,
            targets=None
    ):
        """Request for AssetsApi.bulk_move

        :param source: The UUID of the network currently associated with the assets.
        :param destination: The UUID of the network to associate with the specified assets
        :param targets: The IPv4 addresses of the assets to move. The addresses can be a comma-separated list of values.
        """
        self.source = source
        self.destination = destination
        self.targets = targets
        assert all([self.source, self.destination, self.targets])


class BulkDeleteRequest(BaseRequest):

    def __init__(
            self,
            query=None,
    ):
        """Request for AssetsApi.bulk_delete

        :param query: An object containing the query condition(s) for selecting the assets to delete.
            Note: you can read more about the formatting of this query object in the developer documentation
                  https://developer.tenable.com/reference#assets-bulk-delete
        """
        self.query = query
        assert self.query
