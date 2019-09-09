import pytest


@pytest.mark.vcr()
def test_file_upload(client, fetch_file):
    file = fetch_file
    uploaded_file_name = client.file_api.upload(file)
    assert file.name in uploaded_file_name, u'File name is a part of the returned identifier.'