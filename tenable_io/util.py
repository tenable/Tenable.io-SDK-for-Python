import time

from tenable_io.config import TenableIOConfig

POLLING_INTERVAL = int(TenableIOConfig.get('polling_interval'))


def payload_filter(payload, filter_):
    if callable(filter_):
        payload = {k: v for k, v in payload.items() if filter_(v, k)}
    elif filter:
        payload = {k: v for k, v in payload.items() if v is not None}
    return payload


def wait_until(condition):
    while True:
        if condition():
            return True
        time.sleep(POLLING_INTERVAL)
