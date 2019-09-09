import pytest
import os


@pytest.mark.vcr()
def test_file_helper_upload(client):
    path = 'test_file_upload'
    with open(path, 'a') as fd:
        fd.write('test_file')
    uploaded_file_name = client.file_helper.upload(path)
    assert os.path.basename(path) in uploaded_file_name, u'File name is a part of the returned identifier.'
    os.remove(path)
