import pytest
import xml.etree.ElementTree as ET

from tests.base import BaseTest

from tenable_io.api.models import ScReport


class TestScReportsApi(BaseTest):

    @pytest.fixture(scope='class')
    def container(self, client, image):
        containers = client.sc_containers_api.list()
        yield containers[0]

    def test_show(self, client, container):
        report = client.sc_reports_api.show(container.id)
        assert isinstance(report, ScReport), u'The method returns type.'

    def test_by_image(self, client, image):
        report = client.sc_reports_api.by_image(image['id'])
        assert isinstance(report, ScReport), u'The method returns type.'

    def test_by_image_digest(self, client, image):
        report = client.sc_reports_api.by_image_digest(image['digest'])
        assert isinstance(report, ScReport), u'The method returns type.'

    def test_nessus_show(self, client, container):
        report = client.sc_reports_api.nessus_show(container.id)
        root = ET.fromstring(report)
        assert root.tag == u'NessusClientData_v2', u'The method return a Nessus v2 format file.'
