import socket
import json
from typing import Any, Dict, List
from urllib import parse

from constants import DEFAULT_HTTP_CONTENT_TYPE
from utils import log, parse_content_type, paser_x_www_form_urlencoded, parse_form_data


class Header(dict):
    @property
    def cookies(self):
        data = {}
        cookies = self.get("Cookie", None)
        if not cookies:
            return None
        data = {}
        for cookie in cookies.split("; "):
            k, v = cookie.split("=")
            data[k] = v
        return data


class Request(object):
    def __init__(
        self,
        raw_data: bytes,
    ):
        self.raw_data = raw_data
        (self.head, self.body) = self.raw_data.split(b"\r\n\r\n", 2)
        
        self.url = self.head.split(b" ")[1].decode()

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


def response(request: Request):
    # print(request.method)
    # print(request.url)
    # print(request.protocol)
    # print(request.args)
    return f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{json.dumps(request.headers)}{json.dumps(request.headers.cookies)}".encode("utf-8")


def recv_data(conn):
    """接受所有数据"""
    data = b""
    buffer_size = 1024
    flag = False
    while True:
        if flag:
            break
        d = conn.recv(buffer_size)
        if len(d) < buffer_size:
            flag = True
        data += d
    return data


def handle_request(request: Request):
    return response(request)


def main(host=None, port=None):
    if not host:
        host = "127.0.0.1"
    if not port:
        port = 5000
    # AF_INET: 服务器之间网络通信, SOCK_STREAM: 流式socket , for TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # 接受TCP连接并返回（conn,address）,其中conn是新的套接字对象，可以用来接收和发送数据。address是连接客户端的地址。
        s.bind((host, port))
        # 开始监听TCP传入连接。backlog指定在拒绝连接之前，操作系统可以挂起的最大连接数量。该值至少为1。
        s.listen(5)
        log(f"server start listen {host}:{port}")
        while True:
            conn = None
            try:
                conn, addr = s.accept()
                data = recv_data(conn)
                request = Request(data)
                log(f"[{addr[0]}:{addr[1]}] {request.method} {request.protocol[0]}://{host}:{port}{request.url}")
                response = handle_request(request)
                conn.send(response)
                conn.close()
            except Exception as e:
                print("except", e)
                break
            finally:
                conn.close()
                

if __name__ == "__main__":
    main()
