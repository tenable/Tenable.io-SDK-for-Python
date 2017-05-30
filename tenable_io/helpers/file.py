import os

from tenable_io.exceptions import TenableIOException


class FileHelper(object):

    def __init__(self, client):
        self._client = client

    def upload(self, path):
        """Uploads a file. Usually used along with another API service that requires a file.

        :param path: Path of the file.
        :return: A string identifier for the uploaded file.
        """
        if not os.path.isfile(path):
            raise TenableIOException(u'File does not exist at path.')

        with open(path, 'rb') as upload_file:
            uploaded_file_name = self._client.file_api.upload(upload_file)

        return uploaded_file_name
