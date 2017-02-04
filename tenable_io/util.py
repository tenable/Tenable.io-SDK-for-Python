def payload_filter(payload, filter_):
    if callable(filter_):
        payload = {k: v for k, v in payload.items() if filter_(v, k)}
    elif filter:
        payload = {k: v for k, v in payload.items() if v is not None}
    return payload
