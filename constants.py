from enum import Enum, auto


class HttpMethod(Enum):
    GET = auto()
    POST = auto()
    PUT = auto()
    HEAD = auto()
    OPTIONS = auto()
    PATCH = auto()
    DELETE = auto()


DEFAULT_HTTP_CONTENT_TYPE = "application/octet-stream"
