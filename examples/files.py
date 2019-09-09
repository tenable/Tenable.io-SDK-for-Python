import os

from tenable_io.client import TenableIOClient


def example():

    # Generate a file with an unique name.
    upload_file = u'example_upload'
    with open(upload_file, 'a') as fd:
        fd.write('test_file')

    '''
    Instantiate an instance of the TenableIOClient.
    '''
    client = TenableIOClient()

    '''
    Upload a file (usually used along with another API resource method that requires a file).
    '''
    uploaded_file_name = client.file_helper.upload(upload_file)
    assert uploaded_file_name

    os.remove(upload_file)
