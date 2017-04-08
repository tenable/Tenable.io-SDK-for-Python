class TenableIOException(Exception):

    def __init__(self, message=None, code=None):
        self.code = code if code else TenableIOErrorCode.GENERIC
        self.message = message if message else self.code.description

    def __str__(self):
        return self.message


class TenableIOApiException(TenableIOException):

    def __init__(self, response):
        self.response = response
        code = TenableIOErrorCode.from_http_code(response.status_code)
        if code:
            super(TenableIOApiException, self).__init__(
                response.text if response.text else code.description,
                code
            )
        else:
            super(TenableIOApiException, self).__init__(response.text)


class ErrorCode(object):

    _HTTP_CODES = {}

    def __init__(self, description, http_code=None):
        self.description = description
        self._http_code = http_code
        if self._http_code:
            ErrorCode._HTTP_CODES[self._http_code] = self

    @staticmethod
    def from_http_code(code):
        return ErrorCode._HTTP_CODES.get(code)

    def __str__(self):
        return self.description


class TenableIOErrorCode(ErrorCode):

    GENERIC = ErrorCode("Generic")

    CONTINUE = ErrorCode("Continue", 100)
    SWITCHING_PROTOCOLS = ErrorCode("Switching Protocols", 101)
    PROCESSING = ErrorCode("Processing", 102)
    OK = ErrorCode("OK", 200)
    CREATED = ErrorCode("Created", 201)
    ACCEPTED = ErrorCode("Accepted", 202)
    NON_AUTHORITATIVE_INFORMATION = ErrorCode("Non-authoritative Information", 203)
    NO_CONTENT = ErrorCode("No Content", 204)
    RESET_CONTENT = ErrorCode("Reset Content", 205)
    PARTIAL_CONTENT = ErrorCode("Partial Content", 206)
    MULTI_STATUS = ErrorCode("Multi-Status", 207)
    ALREADY_REPORTED = ErrorCode("Already Reported", 208)
    IM_USED = ErrorCode("IM Used", 226)
    MULTIPLE_CHOICES = ErrorCode("Multiple Choices", 300)
    MOVED_PERMANENTLY = ErrorCode("Moved Permanently", 301)
    FOUND = ErrorCode("Found", 302)
    SEE_OTHER = ErrorCode("See Other", 303)
    NOT_MODIFIED = ErrorCode("Not Modified", 304)
    USE_PROXY = ErrorCode("Use Proxy", 305)
    TEMPORARY_REDIRECT = ErrorCode("Temporary Redirect", 307)
    PERMANENT_REDIRECT = ErrorCode("Permanent Redirect", 308)
    BAD_REQUEST = ErrorCode("Bad Request", 400)
    UNAUTHORIZED = ErrorCode("Unauthorized", 401)
    PAYMENT_REQUIRED = ErrorCode("Payment Required", 402)
    FORBIDDEN = ErrorCode("Forbidden", 403)
    NOT_FOUND = ErrorCode("Not Found", 404)
    METHOD_NOT_ALLOWED = ErrorCode("Method Not Allowed", 405)
    NOT_ACCEPTABLE = ErrorCode("Not Acceptable", 406)
    PROXY_AUTHENTICATION_REQUIRED = ErrorCode("Proxy Authentication Required", 407)
    REQUEST_TIMEOUT = ErrorCode("Request Timeout", 408)
    CONFLICT = ErrorCode("Conflict", 409)
    GONE = ErrorCode("Gone", 410)
    LENGTH_REQUIRED = ErrorCode("Length Required", 411)
    PRECONDITION_FAILED = ErrorCode("Precondition Failed", 412)
    PAYLOAD_TOO_LARGE = ErrorCode("Payload Too Large", 413)
    REQUEST_URI_TOO_LONG = ErrorCode("Request-URI Too Long", 414)
    UNSUPPORTED_MEDIA_TYPE = ErrorCode("Unsupported Media Type", 415)
    REQUESTED_RANGE_NOT_SATISFIABLE = ErrorCode("Requested Range Not Satisfiable", 416)
    EXPECTATION_FAILED = ErrorCode("Expectation Failed", 417)
    IM_A_TEAPOT = ErrorCode("I'm a teapot", 418)
    MISDIRECTED_REQUEST = ErrorCode("Misdirected Request", 421)
    UNPROCESSABLE_ENTITY = ErrorCode("Unprocessable Entity", 422)
    LOCKED = ErrorCode("Locked", 423)
    FAILED_DEPENDENCY = ErrorCode("Failed Dependency", 424)
    UPGRADE_REQUIRED = ErrorCode("Upgrade Required", 426)
    PRECONDITION_REQUIRED = ErrorCode("Precondition Required", 428)
    TOO_MANY_REQUESTS = ErrorCode("Too Many Requests", 429)
    REQUEST_HEADER_FIELDS_TOO_LARGE = ErrorCode("Request Header Fields Too Large", 431)
    CONNECTION_CLOSED_WITHOUT_RESPONSE = ErrorCode("Connection Closed Without Response", 444)
    UNAVAILABLE_FOR_LEGAL_REASONS = ErrorCode("Unavailable For Legal Reasons", 451)
    CLIENT_CLOSED_REQUEST = ErrorCode("Client Closed Request", 499)
    INTERNAL_SERVER_ERROR = ErrorCode("Internal Server Error", 500)
    NOT_IMPLEMENTED = ErrorCode("Not Implemented", 501)
    BAD_GATEWAY = ErrorCode("Bad Gateway", 502)
    SERVICE_UNAVAILABLE = ErrorCode("Service Unavailable", 503)
    GATEWAY_TIMEOUT = ErrorCode("Gateway Timeout", 504)
    HTTP_VERSION_NOT_SUPPORTED = ErrorCode("HTTP Version Not Supported", 505)
    VARIANT_ALSO_NEGOTIATES = ErrorCode("Variant Also Negotiates", 506)
    INSUFFICIENT_STORAGE = ErrorCode("Insufficient Storage", 507)
    LOOP_DETECTED = ErrorCode("Loop Detected", 508)
    NOT_EXTENDED = ErrorCode("Not Extended", 510)
    NETWORK_AUTHENTICATION_REQUIRED = ErrorCode("Network Authentication Required", 511)
    NETWORK_CONNECT_TIMEOUT_ERROR = ErrorCode("Network Connect Timeout Error", 599)
