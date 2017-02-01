import re

from tenable_io.helpers.scan import ScanRef
from tenable_io.api.models import Folder


class FolderHelper(object):

    def __init__(self, client):
        self._client = client

    def folders(self, name_regex=None, name=None, type=None):
        """Retrieve folders.

        :param name_regex: Regular expression to match folder name with, default to None.
        :param name: String to match folder name with, default to None.
        :param type: The type of folders, default to None. (ex. Folder.TYPE_CUSTOM)
        :return: A list of FolderRef instances of all matching folders.
        """
        folders = self._client.folders_api.list().folders
        if name_regex:
            name_regex = re.compile(name_regex)
            folders = [folder for folder in folders if name_regex.match(folder.name)]
        elif name:
            folders = [folder for folder in folders if name == folder.name]
        if type:
            folders = [folder for folder in folders if type == folder.type]
        return [FolderRef(self._client, folder.id) for folder in folders]

    def id(self, id):
        """Retrieve a folder by ID.

        :param id: The folder ID.
        :return: An instance of FolderRef for the folder, None if folder is not found.
        """
        folders = self._client.folders_api.list().folders
        folders = [folder for folder in folders if folder.id == id]
        return folders[0] if len(folders) > 0 else None

    def create(self, name):
        """Create a new folder.

        :param name: The folder name.
        :return: The instance of FolderRef for the newly created folder.
        """
        return FolderRef(self._client, self._client.folders_api.create(name))

    def trash_folder(self):
        """Get the trash folder.

        :return: An instance of FolderRef for the trash folder.
        """
        trash_folders = self.folders(type=Folder.TYPE_TRASH)
        return trash_folders[0] if len(trash_folders) > 0 else None

    def main_folder(self):
        """Get the main folder.

        :return: An instance of FolderRef for the main folder.
        """
        trash_folders = self.folders(type=Folder.TYPE_MAIN)
        return trash_folders[0] if len(trash_folders) > 0 else None


class FolderRef(object):

    def __init__(self, client, id):
        self._client = client
        self.id = id

    def scans(self):
        """Get scans in the folder.

        :return: A list of ScanRef for the scans in the folder.
        """
        return self._client.scan_helper.scans(folder_id=self.id)

    def stop_scans(self):
        """Stop all the scans in the folder.

        :return: The same instance of FolderRef.
        """
        self._client.scan_helper.stop_all(folder=self)
        return self

    def add(self, scan=None, scan_id=None):
        """Add a scan to the folder.

        :param scan: An instance of ScanRef for the scan, default to None.
        :param scan_id: The ID of the scan, default to None.
        :return: The same instance of FolderRef.
        """
        assert scan_id is not None or isinstance(scan, ScanRef)
        if scan_id is not None:
            scan = ScanRef(self._client, scan_id)
        scan.move_to(self)
        return self

    def _info(self):
        return self._client.folder_helper.id(self.id)

    def name(self):
        """Get the folder name.

        :return: The folder name.
        """
        return self._info().name

    def type(self):
        """Get the folder type.

        :return: The folder type.
        """
        return self._info().type

    def delete(self):
        """zDelete the folder.

        :return: The same instance of FolderRef.
        """
        self._client.folders_api.delete(self.id)
        return self
