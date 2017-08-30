import os
import shutil
import uuid
import pytest

from tests.base import BaseTest
from tests.util import upload_image

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

    def session_file_output(self, name, content=None):
        path = u'%s/%s' % (self._output_dir, name)
        if content:
            with open(path, 'a') as fd:
                fd.write('test_file')
        return path

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


@pytest.fixture(scope='session')
def image(app, client):
    i = upload_image(app.session_name(u'test_image_%s'), u'test_image')
    BaseTest.wait_until(lambda: client.sc_test_jobs_api.by_image(i['id']),
                        lambda job: job.job_status == u'completed')
    yield i
    client.sc_containers_api.delete(i['name'], i['digest'])


@pytest.fixture(scope='session')
def vulnerable_image(app, client):
    i = upload_image(app.session_name(u'test_vulnerable_image_%s'), u'test_vulnerable_image', vulnerable=True)
    BaseTest.wait_until(lambda: client.sc_test_jobs_api.by_image(i['id']),
                        lambda job: job.job_status == u'completed')
    yield i
    client.sc_containers_api.delete(i['name'], i['digest'])
