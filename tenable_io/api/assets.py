from tenable_io.api.base import BaseApi
from tenable_io.api.models import AssetsAsset, AssetsAssetList


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
        :return: An instance of :class:`AssetsAsset`.
        """
        response = self._client.get('assets/%(asset_id)s', path_params={'asset_id': asset_id})
        return AssetsAsset.from_json(response.text)
