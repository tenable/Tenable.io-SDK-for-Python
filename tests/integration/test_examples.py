from tests.base import BaseTest
from tests.config import TenableIOTestConfig


class TestExamples(BaseTest):

    def test_exports(self, app):
        from examples.exports import example
        example(app.session_file_output)

    def test_file(self, app):
        from examples.files import example
        example(app.session_file_output)

    def test_folders(self, app):
        from examples.folders import example
        example(app.session_name)

    def test_policies(self, app):
        from examples.policies import example
        example(app.session_name, app.session_file_output)

    def test_scans(self, app):
        from examples.scans import example
        example(app.session_name, app.session_file_output, TenableIOTestConfig.get('scan_text_targets'))

    def test_workbench(self, app):
        from examples.workbench import example
        example(app.session_file_output)
