import os
import pytest
import shutil
import uuid

from tenable_io.client import TenableIOClient


class App:

    def __init__(self):
        self._uuid = uuid.uuid4()
        self._output_dir = self.session_name('./._tests_')
        os.makedirs(self._output_dir)

    def session_name(self, name, length=8):
        try:
            session_name = name % self._uuid.hex[:length]
        except TypeError:
            session_name = u'%s_%s' % (name, self._uuid.hex[:length])
        return session_name

    def session_file_output(self, name):
        return u'%s/%s' % (self._output_dir, name)

    def tear_down(self):
        shutil.rmtree(self._output_dir)


@pytest.fixture(scope='session')
def app():
    a = App()
    yield a
    a.tear_down()


@pytest.fixture(scope='session')
def client():
    yield TenableIOClient()
