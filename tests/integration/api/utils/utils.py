import base64
import hashlib
import json
import requests

from time import sleep, time

from tenable_io.config import TenableIOConfig
from tests.config import TenableIOTestConfig

WAIT_TIMEOUT = 300
WAIT_INTERVAL = 10


def wait_until(expression, condition):
    value = expression()
    start_time = time()
    elapsed = 0
    while not condition(value) and elapsed <= WAIT_TIMEOUT:
        sleep(WAIT_INTERVAL)
        value = expression()
        elapsed = time() - start_time
    assert condition(value), u'Timeout waiting for a condition (%d seconds elapsed).' % elapsed
    return value


def upload_image(name, tag, vulnerable=False):

    host = TenableIOTestConfig.get('registry_host')

    file_path = './tests/docker_images/scratch.tgz'
    digest_tar = u'sha256:188307c3217788f441fa8a31e1bdbc4b4286a12b12da90038a8b1e22241176c5'  # tar
    digest_tgz = u'sha256:96626451b6947696c15b96333de54fd329f8f8cb5073163ef881153b37aafe7d'  # tgz

    if vulnerable:
        file_path = './tests/docker_images/alpine_3_1.tgz'
        digest_tar = u'sha256:534a5cc0b456e6d82b52614ef3a731e2afc19c89f991c11b41d364727bea7c2d'  # tar
        digest_tgz = u'sha256:57735dd315307043f9d21fe748f1c5bab781514b4db2c7f8cbac34ba39331178'  # tgz

    '''
    Get authorization token for the session.
    '''
    response = requests.get(
        host + '/v2/token',
        headers={
            u'Authorization': u'Basic %s' % base64.b64encode(
                (u'%s:%s' % (TenableIOConfig.get(u'access_key'), TenableIOConfig.get(u'secret_key')))
                .encode('utf-8')).decode('utf-8')
        },
        params={u'service': u'tenable.io'}
    )
    token = json.loads(response.text)[u'token']

    session = requests.Session()
    session.headers.update({
        u'Authorization': u'Bearer %s' % token,
    })

    '''
    Get upload URL for the layer.
    '''
    response = session.post(
        host + '/v2/{name}/blobs/uploads/'.format(name=name),
        headers={
            u'Content-Type': u'application/x-www-form-urlencoded'  # Errors without Content-Type for some reason.
        })
    upload_url = response.headers[u'Location']

    '''
    Upload the layer as tar-gzip.
    '''
    data = open(file_path, 'rb').read()
    session.put(
        upload_url,
        params={u'digest': digest_tgz},
        headers={u'Content-Type': u'application/vnd.docker.image.rootfs.diff.tar.gzip'},
        data=data
    )

    '''
    Get the layer length.
    '''
    response = session.head(host + '/v2/{name}/blobs/{digest}'.format(name=name, digest=digest_tgz))
    data_size = int(response.headers[u'Content-Length'])

    '''
    Get upload URL for the config.
    '''
    response = session.post(
        host + '/v2/{name}/blobs/uploads/'.format(name=name),
        headers={
            u'Content-Type': u'application/x-www-form-urlencoded'  # Errors without Content-Type for some reason.
        })
    upload_url = response.headers[u'Location']

    '''
    Upload the config.
    '''
    obj = {
        u'architecture': u'amd64',
        u'config': {},
        u'created': u'1970-01-01T00:00:01Z',
        u'os': u'linux',
        u'history': [{
            u'created': u'1970-01-01T00:00:01Z'
        }],
        u'rootfs': {
            u'type': u'layers',
            u'diff_ids': [digest_tar]
        }
    }

    data = json.dumps(obj).encode(u'utf8')
    config_digest = u'sha256:%s' % hashlib.sha256(data).hexdigest()

    session.put(
        upload_url,
        params={u'digest': config_digest},
        headers={u'Content-Type': u'application/vnd.docker.container.image.v1+json'},
        data=data
    )

    '''
    Get the config length.
    '''
    response = session.head(host + '/v2/{name}/blobs/{digest}'.format(name=name, digest=config_digest))
    config_size = int(response.headers[u'Content-Length'])

    '''
    Upload the manifest.
    '''
    obj = {
        u'schemaVersion': 2,
        u'mediaType': u'application/vnd.docker.distribution.manifest.v2+json',
        u'config': {
            u'mediaType': u'application/vnd.docker.container.image.v1+json',
            u'size': config_size,
            u'digest': config_digest  # the image ID
        },
        u'layers': [
            {
                u'mediaType': u'application/vnd.docker.image.rootfs.diff.tar.gzip',
                u'size': data_size,
                u'digest': digest_tgz
            }
        ]
    }

    manifest = json.dumps(obj).encode(u'utf8')

    response = session.put(
        host + '/v2/{name}/manifests/{reference}'.format(name=name, reference=tag),
        headers={u'Content-Type': u'application/vnd.docker.distribution.manifest.v2+json'},
        data=manifest
    )
    manifest_digest = response.headers[u'Docker-Content-Digest']

    return {
        'name': name,
        'tag': tag,
        'id': config_digest.split(u'sha256:')[1][:12],
        'digest': manifest_digest.split(u'sha256:')[1],
    }
