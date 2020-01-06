import pytest

from tenable_io.api.networks import NetworkRequest, BulkAssignRequest
from tenable_io.api.models import Network, NetworkList, ScannerList


@pytest.mark.vcr()
def test_networks_list(client):
    networks = client.networks_api.list()
    assert isinstance(networks, NetworkList), u'The `list` method did not return type `NetworkList`.'


@pytest.mark.vcr()
def test_networks_details(client):
    network = client.networks_api.details('00000000-0000-0000-0000-000000000000') # default network uuid
    assert isinstance(network, Network), u'The `details` method did not return type `Network`.'


@pytest.mark.vcr()
def test_networks_create(client):
    network = client.networks_api.create(NetworkRequest(name="test_network", description="automated_test"))
    assert isinstance(network, Network), u'The `create` method did not return type `Network`.'


@pytest.mark.vcr()
def test_networks_update(client):
    network = client.networks_api.create(NetworkRequest(name="test_network2", description="automated_test"))
    network = client.networks_api.update(network.uuid, NetworkRequest(name="updated_network_name"))
    assert isinstance(network, Network), u'The `update` method did not return type `Network`.'
    assert network.name == 'updated_network_name', u'Expected the network name to be updated.'


@pytest.mark.vcr()
def test_networks_delete(client):
    network = client.networks_api.create(NetworkRequest(name="test_network3", description="automated_test"))
    assert client.networks_api.delete(network.uuid)


@pytest.mark.vcr()
def test_networks_list_scanners(client):
    networks = client.networks_api.list()
    scanners = client.networks_api.list_scanners(networks.networks[0].uuid)
    assert isinstance(scanners, ScannerList), u'The `list_scanners` method did not return type `ScannerList`.'


@pytest.mark.vcr()
def test_networks_list_assignable_scanners(client):
    networks = client.networks_api.list()
    scanners = client.networks_api.list_assignable_scanners(networks.networks[1].uuid)
    assert isinstance(scanners, ScannerList), u'The `list_scanners` method did not return type `ScannerList`.'
    assert len(scanners.scanners) > 0, u'Expected at least 1 assignable scanner.'


@pytest.mark.vcr()
def test_networks_assign_scanner(client):
    networks = client.networks_api.list()
    scanners = client.networks_api.list_assignable_scanners(networks.networks[1].uuid)
    assert client.networks_api.assign_scanner(network_id=networks.networks[1].uuid,
                                              scanner_uuid=scanners.scanners[0].uuid)


@pytest.mark.vcr()
def test_networks_bulk_assign_scanners(client):
    networks = client.networks_api.list()
    scanners = client.networks_api.list_assignable_scanners(networks.networks[1].uuid)
    assert client.networks_api.bulk_assign_scanners(network_id=networks.networks[1].uuid,
                                                    bulk_assign=BulkAssignRequest(
                                                        scanner_uuids=[scanners.scanners[0].uuid]
                                                    ))
