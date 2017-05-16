import re
import six
import socket
import time

from tenable_io.config import TenableIOConfig

POLLING_INTERVAL = int(TenableIOConfig.get('polling_interval'))
RE_MAC = re.compile('[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$')


def is_ipv4(value):
    """Utility function to detect if a value is a valid IPv4

        :param value: The value to match against.
        :return: True if the value is a valid IPv4.
    """
    try:
        socket.inet_pton(socket.AF_INET, value)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(value)
        except socket.error:
            return False
        return value.count('.') == 3
    except socket.error:  # not a valid address
        return False
    return True


def is_mac(value):
    """Utility function to detect if a value is a valid MAC address.

        :param value: The value to match against.
        :return: True if the value is a valid MAC address.
    """
    return isinstance(value, six.string_types) and \
        RE_MAC.match(value.lower())


def payload_filter(payload, filter_):
    if callable(filter_):
        payload = {k: v for k, v in payload.items() if filter_(v, k)}
    elif filter:
        payload = {k: v for k, v in payload.items() if v is not None}
    return payload


def wait_until(condition, context=None):
    """Utility function to wait for a condition to become True.

        :param condition: The condition function that should evaluate to True if and only if the condition is met.
        :param context: If it is not None, it is passed to every call to the condition function.
        :return: True when the condition function evaluates to True.
    """
    while True:
        if context is not None and condition(context):
            return True
        elif context is None and condition():
            return True
        time.sleep(POLLING_INTERVAL)
