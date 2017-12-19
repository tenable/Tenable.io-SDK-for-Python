from json import loads

from tenable_io.api.base import BaseApi, BaseRequest
from tenable_io.api.models import ImportAsset, ImportAssetJob, ImportAssetJobs


class ImportApi(BaseApi):

    def assets(self, assets_request):
        """Creates job to import assets.

        :param assets_request: An instance of :class:`AssetsRequest`.
        :raise TenableIOApiException:  When API error is encountered.
        :return: The ID of asset import job.
        """
        response = self._client.post('import/assets', assets_request)
        return loads(response.text).get('asset_import_job_uuid')

    def asset_jobs(self):
        """Get list of asset jobs.

        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.ImportAssetJobs`.
        """
        response = self._client.get('import/asset-jobs')
        return ImportAssetJobs.from_json(response.text)

    def asset_job(self, asset_import_job_id):
        """Get specified asset job.

        :param asset_import_job_id: The asset import job id.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.ImportAssetJob`.
        """
        response = self._client.get('import/asset-jobs/%(asset_import_job_id)s',
                                    path_params={
                                        'asset_import_job_id': asset_import_job_id
                                    })
        return ImportAssetJob.from_json(response.text)


class ImportAssetsRequest(BaseRequest):

    def __init__(
            self,
            assets,
            source
    ):
        """Request for ImportApi.assets.

        :param assets: List of assets to import.
        :type assets: list[:class:`tenable_io.api.models.ImportAsset`].
        :param source: Source of assets.
        :type source: string.
        """
        self.assets = assets
        self.source = source

    def as_payload(self, filter_=None):
        payload = super(ImportAssetsRequest, self).as_payload(True)
        assets_payload = [a.as_payload() for a in self.assets if isinstance(a, ImportAsset)]
        if assets_payload:
            payload.__setitem__('assets', assets_payload)
        else:
            payload.pop('assets', None)
        return payload
