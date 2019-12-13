import pytest

from tests.base import BaseTest
from tests.config import TenableIOTestConfig

@pytest.mark.extended_testing
class TestExamples(BaseTest):

    @pytest.mark.vcr()
    def test_exports(self):
        from examples.exports import example
        example()

    @pytest.mark.vcr()
    def test_file(self):
        from examples.files import example
        example()

    @pytest.mark.vcr()
    def test_folders(self):
        from examples.folders import example
        example()

    @pytest.mark.vcr()
    def test_policies(self):
        from examples.policies import example
        example()

    @pytest.mark.skip
    @pytest.mark.vcr()
    def test_scans(self):
        from examples.scans import example
        example(TenableIOTestConfig.get('scan_text_targets'))

    @pytest.mark.vcr()
    def test_users(self):
        from examples.users import example
        example(TenableIOTestConfig.get('users_domain_name'))

    @pytest.mark.vcr()
    def test_workbench(self):
        from examples.workbench import example
        example()
