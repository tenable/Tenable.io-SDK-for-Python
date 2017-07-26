from tests.base import BaseTest
from tests.util import upload_image

from tenable_io.api.models import ScContainer


class TestScContainersApi(BaseTest):

    def test_delete(self, app, client):
        image = upload_image(app.session_name(u'test_sc_containers_delete_%s'), u'test_sc_containers_delete')

        response = client.sc_containers_api.delete(image['name'], image['digest'])

        assert response[u'status'] == u'deleted', u'Correct status for a successful deletion.'

        containers = client.sc_containers_api.list()
        match = [c for c in containers if image['name'].endswith(c.name) and c.digest == u'sha256:%s' % image['digest']]
        assert len(match) == 0, u'The image no longer exists.'

    def test_list(self, client, image):
        containers = client.sc_containers_api.list()

        assert len(containers) > 0, u'At least one image exists.'
        assert isinstance(containers[0], ScContainer), u'The method returns container list.'

        match = [c for c in containers if image['name'].endswith(c.name) and c.digest == u'sha256:%s' % image['digest']]
        assert len(match) == 1, u'The test image exists.'
