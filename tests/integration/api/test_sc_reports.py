import pytest

import xml.etree.ElementTree as ET

from tenable_io.api.models import ScReport
from tests.integration.api.utils.utils import upload_image


@pytest.mark.skip('Deprecated v1 API')
@pytest.mark.vcr()
def test_sc_reports_show(client, fetch_container):
    report = client.sc_reports_api.show(fetch_container.id)
    assert isinstance(report, ScReport), u'The method returns type.'


@pytest.mark.skip('Deprecated v1 API')
@pytest.mark.vcr()
def test_sc_reports_nessus_show(client, fetch_container):
    report = client.sc_reports_api.nessus_show(fetch_container.id)
    root = ET.fromstring(report)
    assert root.tag == u'NessusClientData_v2', u'The method return a Nessus v2 format file.'


@pytest.mark.skip('Deprecated v1 API')
@pytest.mark.vcr()
def test_sc_reports_by_image(client):
    image = upload_image('test_sc_reports_image', 'test_sc_reports_image')
    report = client.sc_reports_api.by_image(image['id'])
    assert isinstance(report, ScReport), u'The method returns type.'


@pytest.mark.skip('Deprecated v1 API')
@pytest.mark.vcr()
def test_sc_reports_by_image_digest(client):
    image = upload_image('test_sc_reports_image_digest', 'test_sc_reports_image_digest')
    report = client.sc_reports_api.by_image_digest(image['digest'])
    assert isinstance(report, ScReport), u'The method returns type.'
