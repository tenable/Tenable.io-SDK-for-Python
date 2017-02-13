import pytest
import types

from tests.base import BaseTest


class TestWorkbenchHelper(BaseTest):

    @pytest.fixture(scope='class')
    def date_range(self):
        """
        The number of days of data prior.
        """
        yield 30

    @pytest.fixture(scope='class')
    def asset(self, client, date_range):
        """
        Asset for testing (if exists).
        """
        assets = next(client.workbench_helper.assets(date_range, page_size=0))
        yield assets[0] if len(assets) > 0 else None

    @pytest.fixture(scope='class')
    def vulnerability(self, client, date_range):
        """
        Vulnerability for testing (if exists).
        """
        vulnerabilities = next(client.workbench_helper.vulnerabilities(date_range, page_size=0))
        yield vulnerabilities[0] if len(vulnerabilities) > 0 else None

    def test_assets(self, client, date_range):
        assets_iter = client.workbench_helper.assets(date_range)
        assert isinstance(assets_iter, types.GeneratorType), u'Returns a generator.'
        assets_iter.close()

    def test_vulnerabilities(self, client, date_range):
        vulnerabilities_iter = client.workbench_helper.vulnerabilities(date_range)
        assert isinstance(vulnerabilities_iter, types.GeneratorType), u'Returns a generator.'
        vulnerabilities_iter.close()

    def test_assets_by_vulnerability_and_vulnerabilities_by_asset(self, client, date_range, vulnerability):
        # No vulnerability, no test.
        if vulnerability is not None:
            assets = next(client.workbench_helper.assets(date_range, plugin_id=vulnerability.plugin_id, page_size=0))
            assert len(assets) > 0, u'Should be at least one asset.'

            asset_id = assets[0].asset.host_uuid
            vulnerabilities = next(client.workbench_helper.vulnerabilities(date_range, asset_id=asset_id, page_size=0))
            assert len(vulnerabilities) > 0, u'Should be at least one vulnerability.'

            assert vulnerability.plugin_id in [v.plugin_id for v in vulnerabilities], \
                u'Vulnerability used to find the asset should be in this asset\'s list of vulnerabilities.'

    def test_vulnerabilities_by_asset(self, client, date_range, asset):
        # No asset, no test.
        if asset is not None:
            vulnerabilities = next(client.workbench_helper.vulnerabilities(
                date_range, asset_id=asset.asset.host_uuid, page_size=0))
            assert isinstance(vulnerabilities, list), u'Should be a list.'
