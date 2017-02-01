from tenable_io.util import payload_filter


class BaseApi(object):

    def __init__(self, client):
        self._client = client


class BaseRequest(object):

    def as_payload(self, filter_=None):
        return payload_filter(self.__dict__, filter_)
