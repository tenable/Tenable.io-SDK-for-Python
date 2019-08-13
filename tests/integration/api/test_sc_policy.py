import pytest

from tests.integration.api.utils.utils import upload_image, wait_until


@pytest.mark.skip('Deprecated v1 API')
@pytest.mark.vcr()
def test_sc_policy_compliance(client):
    image = upload_image('test_sc_policy_compliance', 'test_sc_policy_compliance')
    policy = wait_until(lambda: client.sc_policy_api.compliance(image['id']),
                        lambda response: response[u'status'] != u'error')
    assert policy[u'status'] in [u'pass', u'fail'], \
        u'Status should be either pass or fail based on the policy'
