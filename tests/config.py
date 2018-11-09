from os import environ
import six

if six.PY34:
    import configparser
else:
    import ConfigParser as configparser

base_config = {
    'wait_timeout': environ.get('TENABLEIOTEST_WAIT_TIMEOUT', '800'),
    'scan_template_name': environ.get('TENABLEIOTEST_SCAN_TEMPLATE_NAME', 'basic'),
    'registry_host': environ.get('TENABLEIOTEST_REGISTRY_HOST', 'https://registry.cloud.tenable.com'),
}

# Read tenable_io.ini config. Default to environment variables if exist.
config = configparser.SafeConfigParser(base_config)
config.add_section('tenable_io-test')
config.read('tenable_io.ini')


class TenableIOTestConfig(object):

    @staticmethod
    def get(key):
        return config.get('tenable_io-test', key)
