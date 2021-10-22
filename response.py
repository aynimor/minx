from typing import Dict, Union
from json import dumps as json_dumps
from urllib.parse import quote_plus

from compat import Header


class HTTPResponse():
    def __init__(
        self,
        body: str = None, 
        status: int = 200,
        headers: Dict[str, str] = None,
        content_type: str = None,
    ):
        self.content_type: str = content_type
        self.body = self._encode_body(body)
        self.status = status
        self.headers = Header(headers or {})
        self._cookies = None
        super().__init__()
    
    def _encode_body(self, body):
        if body is None:
            return b""
        else:
            return body.encode() if hasattr(body, "encode") else body
    
    def __repr__(self) -> str:
        return self.__str__()


def json(
    body: dict,
    status: int = 200,
    headers: Dict[str, str] = None,
    content_type: str = "application/json",
    **kwargs,
) -> HTTPResponse:
    return HTTPResponse(
        json_dumps(body, **kwargs),
        headers=headers,
        status=status,
        content_type=content_type,
    )


def text(
    body: str,
    status: int = 200,
    headers: Dict[str, str] = None,
    content_type: str = "text/plain; charset=utf-8",
) -> HTTPResponse:
    if not isinstance(body, str):
        raise TypeError(f"错误的响应类型. 需要 str 类型, 传入 {type(body).__name__})")

    return HTTPResponse(
        body, status=status, headers=headers, content_type=content_type
    )


def html(
    body: Union[str, bytes],
    status: int = 200,
    headers: Dict[str, str] = None,
) -> HTTPResponse:
    return HTTPResponse(  # type: ignore
        body,
        status=status,
        headers=headers,
        content_type="text/html; charset=utf-8",
    )


def redirect(
    to: str,
    headers: Dict[str, str] = None,
    status: int = 302,
    content_type: str = "text/html; charset=utf-8",
) -> HTTPResponse:
    headers = headers or {}

    # URL Quote the URL before redirecting
    safe_to = quote_plus(to, safe=":/%#?&=@[]!$&'()*+,;")

    # According to RFC 7231, a relative URI is now permitted.
    headers["Location"] = safe_to

    return HTTPResponse(
        status=status, headers=headers, content_type=content_type
    )
