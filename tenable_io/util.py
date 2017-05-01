import time

from tenable_io.config import TenableIOConfig

POLLING_INTERVAL = int(TenableIOConfig.get('polling_interval'))


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
