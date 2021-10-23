from typing import Any, Dict, List
from urllib import parse
import json

from constants import DEFAULT_HTTP_CONTENT_TYPE
from compat import Header
from utils import parse_content_type, paser_x_www_form_urlencoded, parse_form_data


class Request(object):
    def __init__(
        self,
        raw_data: bytes,
    ):
        self.raw_data = raw_data
        (self.head, self.body) = self.raw_data.split(b"\r\n\r\n", 2)
        
        self._parsed_protocol: Dict[str, Any] = None
        self._parsed_method: Dict[str, Any] = None
        self._parsed_url: Dict[str, Any] = None
        self.urlparse: Dict[str, Any] = parse.urlparse(self.head.split(b" ")[1].decode())

        self._parsed_json: Dict[str, Any] = None
        self._parsed_form: Dict[str, Any] = None
        self._parsed_file: Dict[str, List[Any]] = None
        self._parsed_args: Dict[str, List[Any]] = None
        self._parsed_headers: Header = None
    
    @property
    def method(self):
        if not self._parsed_method:
            try:
                self._parsed_method = self.head.split(b" ")[0].decode()
            except Exception:
                return None
        return self._parsed_method
    
    @property
    def protocol(self):
        if not self._parsed_protocol:
            try:
                self._parsed_protocol = self.head.split(b" ")[2].decode().split("/")
            except Exception:
                return None
        return self._parsed_protocol
    
    @property
    def url(self):
        if not self._parsed_url:
            try:
                self._parsed_url = self.urlparse.path
            except Exception:
                return None
        return self._parsed_url
    
    @property
    def json(self):
        if not self._parsed_json:
            try:
                self._parsed_json = json.loads(self.body.decode("utf-8"))
            except Exception:
                return None
        return self._parsed_json

    @property
    def form(self):
        if not self._parsed_form:
            self
            content_type = self.headers.get("Content-Type", DEFAULT_HTTP_CONTENT_TYPE)
            content_type, parameter = parse_content_type(content_type)
            if content_type == "application/x-www-form-urlencoded":
                self._parsed_form = paser_x_www_form_urlencoded(self.body.decode("utf-8"))
            elif content_type == "multipart/form-data":
                self._parsed_files = parse_form_data(self.body, parameter)
        return self._parsed_form
    
    @property
    def files(self):
        if not self._parsed_files:
            self.form
        return self._parsed_files
    
    @property
    def args(self):
        if not self._parsed_args:
            self._parsed_args = {}
            for arg in self.urlparse.query.split("&"):
                k, v = arg.split("=")
                self._parsed_args[k] = v
        return self._parsed_args
    
    @property
    def headers(self):
        if not self._parsed_headers:
            self._parsed_headers = Header()
            headers = self.head.split(b"\r\n")[1:]
            for header in headers:
                key, value = header.decode("utf-8").split(": ")
                self._parsed_headers[key] = value
        return self._parsed_headers
