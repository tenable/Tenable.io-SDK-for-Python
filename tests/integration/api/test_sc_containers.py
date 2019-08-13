import pytest

from tenable_io.api.models import ScContainer

from tests.integration.api.utils.utils import upload_image


@pytest.mark.vcr()
def test_sc_containers_delete(client):
    image = upload_image('test_sc_containers_delete', 'test_sc_containers_delete')

    response = client.sc_containers_api.delete(image['name'], image['digest'])

    assert response[u'status'] == u'deleted', u'The container was not deleted.'

    containers = client.sc_containers_api.list()
    match = [c for c in containers if image['name'].endswith(c.name) and c.digest == u'sha256:%s' % image['digest']]
    assert len(match) == 0, u'The image still exists.'


@pytest.mark.vcr()
def test_sc_containers_list(client):
    image = upload_image('test_sc_containers_list', 'test_sc_containers_list')
    containers = client.sc_containers_api.list()

    assert len(containers) > 0, u'Expected at least one image to exist.'
    assert isinstance(containers[0], ScContainer), u'The method returns container list.'

    match = [c for c in containers if image['name'].endswith(c.name) and c.digest == u'sha256:%s' % image['digest']]
    assert len(match) == 1, u'The test image exists.'
