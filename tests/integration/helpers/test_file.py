import pytest
import os

from tests.base import BaseTest


class TestFileHelper(BaseTest):

    @pytest.fixture(scope='class')
    def path(self, app):
        """
        Create a path to a file for testing.
        """
        path = app.session_file_output('test_file', 'test_file')
        yield path
        os.remove(path)

    def test_upload(self, client, path):
        uploaded_file_name = client.file_helper.upload(path)
        assert os.path.basename(path) in uploaded_file_name, u'File name is a part of the returned identifier.'
