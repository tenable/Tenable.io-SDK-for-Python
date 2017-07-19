from tests.base import BaseTest


class TestScPolicyApi(BaseTest):

    def test_compliance(self, client, image):
        policy = self.wait_until(lambda: client.sc_policy_api.compliance(image['id']),
                                 lambda response: response[u'status'] != u'error')
        assert policy[u'status'] in [u'pass', u'fail'], \
            u'Status should be either pass or fail based on the policy'
