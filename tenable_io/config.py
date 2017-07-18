from os import environ
import six

if six.PY34:
    import configparser
else:
    import ConfigParser as configparser

base_config = {
    'endpoint': environ.get('TENABLEIO_ENDPOINT', 'https://cloud.tenable.com/'),
    'access_key': environ.get('TENABLEIO_ACCESS_KEY'),
    'secret_key': environ.get('TENABLEIO_SECRET_KEY'),
    'logging_level': environ.get('TENABLEIO_LOGGING_LEVEL', 'WARNING'),
    'polling_interval': environ.get('TENABLEIO_POLLING_INTERVAL', '10'),
    'max_retries': environ.get('TENABLEIO_MAX_RETRIES', '3'),
}

# Read tenable_io.ini config. Default to environment variables if exist.
config = configparser.SafeConfigParser(base_config)
config.add_section('tenable_io')
config.read('tenable_io.ini')


class TenableIOConfig(object):

    @staticmethod
    def get(key):
        return config.get('tenable_io', key)
