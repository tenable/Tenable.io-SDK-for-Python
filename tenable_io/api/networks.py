from tenable_io.api.base import BaseApi, BaseRequest
from tenable_io.api.models import Network, NetworkList, ScannerList


class NetworksApi(BaseApi):

    def create(self, network_request):
        """Creates a network object that you associate with scanners and scanner groups.

        :param network_request: An instance of :class:`NetworkRequest`.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.Network`.
        """
        response = self._client.post('networks', network_request)
        return Network.from_json(response.text)

    def list(self, f=None, ft='and', limit=None, offset=0, sort=None, includeDeleted=False):
        """Returns a list of Networks.

        :param f: A list of :class:`tenable_io.api.models.AssetFilter` instances.
        :param ft: The action to apply if multiple 'f' parameters are provided. Supported values are **and** and **or**.
        :param limit: The maximum number of records to be retrieved.
        :param offset: The offset from request.
        :param sort: A list of fields on which the results are sorted.
        :param includeDeleted: boolean - whether the response should include deleted networks.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.NetworkList`.
        """
        fgen = (i.field + ':' + i.operator + ':' + i.value for i in f) if f is not None else None
        response = self._client.get('networks',
                                    params={'f': '&'.join(fgen) if fgen is not None else None,
                                            'ft': ft if fgen is not None else None,
                                            'limit': limit,
                                            'offset': offset,
                                            'sort': ','.join(sort) if sort is not None else None,
                                            'includeDeleted': includeDeleted})
        return NetworkList.from_json(response.text)

    def details(self, network_id):
        """Returns the details of the specified network object.

        :param network_id: The UUID of the network object for which you want to view details.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.Network`.
        """
        response = self._client.get('networks/%(network_id)s', path_params={'network_id': network_id})
        return Network.from_json(response.text)

    def delete(self, network_id):
        """Delete a network.

        :param network_id: The UUID of the network object to delete.
        :raise TenableIOApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.delete('networks/%(network_id)s', path_params={'network_id': network_id})
        return True

    def update(self, network_id, network_request):
        """Update a network.

        :param network_id: The UUID of the network object to update.
        :param network_request: An instance of :class:`NetworkRequest`.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.Network`.
        """
        response = self._client.put('networks/%(network_id)s',
                                    payload=network_request,
                                    path_params={'network_id': network_id})
        return Network.from_json(response.text)

    def assign_scanner(self, network_id, scanner_uuid):
        """Associates a scanner or scanner group with a network object.

        :param network_id: The UUID of the network object to assign scanners to.
        :param scanner_uuid: The UUID of the scanner or scanner group you want to assign to the network object.
        :raise TenableIOApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.post('networks/%(network_id)s/scanners/%(scanner_uuid)s',
                          path_params={'network_id': network_id, 'scanner_uuid': scanner_uuid})
        return True

    def list_scanners(self, network_id):
        """Lists all scanners and scanner groups belonging to the specified network object.

        :param network_id: The UUID of the network object for which you want to view scanners.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.ScannerList`.
        """
        response = self._client.get('networks/%(network_id)s/scanners', path_params={'network_id': network_id})
        return ScannerList.from_json(response.text)

    def bulk_assign_scanners(self, network_id, bulk_assign):
        """Bulk assigns scanners and scanner groups to a custom network.

        :param network_id: The UUID of the network object to assign scanners to.
        :param bulk_assign: An instance of :class:`BulkAssignRequest`.
        :raise TenableIOApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.post('networks/%(network_id)s/scanners',
                          payload=bulk_assign,
                          path_params={'network_id': network_id})
        return True

    def list_assignable_scanners(self, network_id):
        """Lists all scanners and scanner groups not yet assigned to network object.

        :param network_id: The UUID of the network you wish to assign scanners to.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.ScannerList`.
        """
        response = self._client.get('networks/%(network_id)s/assignable-scanners',
                                    path_params={'network_id': network_id})
        return ScannerList.from_json(response.text)


class NetworkRequest(BaseRequest):

    def __init__(
            self,
            name=None,
            description=None,
    ):
        self.name = name
        self.description = description

        assert self.name


class BulkAssignRequest(BaseRequest):

    def __init__(
            self,
            scanner_uuids=[],
    ):
        self.scanner_uuids = scanner_uuids
