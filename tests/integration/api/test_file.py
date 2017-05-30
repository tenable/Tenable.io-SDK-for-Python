import pytest

from six import StringIO

from tests.base import BaseTest


class TestFileApi(BaseTest):

    @pytest.fixture(scope='class')
    def file(self, app):
        file = StringIO(app.session_name('test content'))
        setattr(file, 'name', app.session_name('test_file'))
        yield file

    def test_upload(self, client, file):
        uploaded_file_name = client.file_api.upload(file)
        assert file.name in uploaded_file_name, u'File name is a part of the returned identifier.'
