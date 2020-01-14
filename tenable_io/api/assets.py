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

    def update_acr(self, bulk_acr):
        """Bulk updates ACR scores for assets.

        Note: This API required Admin [64] permissions.

        :param bulk_acr: An instance of :class:`BulkACRRequest`.
        :return: True if successful
        """
        self._client.post('api/v2/assets/bulk-jobs/acr', bulk_acr)
        return True


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


class BulkACRRequest(BaseRequest):

    REASON_BUSINESS_CRITICAL = u'Business Critical'
    REASON_IN_SCOPE_FOR_COMPLIANCE = u'In Scope For Compliance'
    REASON_EXISTING_MITIGATION_CONTROL = u'Existing Mitigation Control'
    REASON_DEV_ONLY = u'Dev only'
    REASON_KEY_DRIVERS_DO_NOT_MATCH = u'Key drivers does not match'
    REASON_OTHER = u'Other'

    _valid_reasons = {
        REASON_BUSINESS_CRITICAL,
        REASON_IN_SCOPE_FOR_COMPLIANCE,
        REASON_EXISTING_MITIGATION_CONTROL,
        REASON_DEV_ONLY,
        REASON_KEY_DRIVERS_DO_NOT_MATCH,
        REASON_OTHER
    }

    def __init__(
            self,
            acr_score=None,
            reason=None,
            note=None,
            asset=None,
    ):
        """Request for AssetsApi.update_acr

        Note: this method only supports asset id as the identifier and can only utilize a single acr score per request.

        :param acr_score: The ACR score you want to assign to the asset. The ACR must be an integer from 1 to 10.
        :param reason: The reasons you are updating the ACR for the assets. This must be a list of type str.
        :param note: Any notes you want to add to clarify the circumstances behind the update. Should be type str.
        :param asset: The identifiers of the assets to update to the specified ACR. Should be a list of UUIDs.
        """
        if acr_score is None or not isinstance(acr_score, int) or 10 < acr_score < 1:
            raise AttributeError('"acr_score" must be an int between 1 and 10.')
        if reason is not None and isinstance(reason, list):
            for r in reason:
                if r not in BulkACRRequest._valid_reasons:
                    raise AttributeError('"reason" must be a valid reason. '
                                         'See https://developer.tenable.com/reference#assets-bulk-update-acr')
        if asset is None or not isinstance(reason, list):
            raise AttributeError('"asset" must be specified.')

        self.acr_score = acr_score
        self.reason = reason
        self.note = note
        self.asset = [{'id': a} for a in asset]

    def as_payload(self, filter_=None):
        return [super(BulkACRRequest, self).as_payload(True)]
