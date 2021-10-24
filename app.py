from .server import run_server

from .request import Request
from .utils import log
from .response import text, HTTPResponse

class Minx():
    def __init__(self, config: dict=None):
        self.router_map = {}
        self.configs = {}
        if config:
            self.configs.update(config)
    
    def add_route(self, handler, uri: str, methods: set = {"GET"}):
        if uri in self.router_map:
            raise Exception("已注册相同uri")
        self.router_map[uri] = {"methods": set(map(lambda x: x.upper(), methods)), "handler": handler}
    
    def get_route(self, uri: str, method: str):
        if uri not in self.router_map:
            return None
        if method not in self.router_map[uri]["methods"]:
            return None
        return self.router_map[uri]["handler"]

    def run(self, host, port):
        log(f"start server in {host}:{port}")
        run_server(host, port, self)

    def handle_request(self, request: Request):
        handler = self.get_route(request.url, request.method)
        if handler is None:
            return text("404 Not Found", status=404)

        resp = handler(request)
        if resp is None:
            return text("Internal Server Error", status=500)

        return resp
    
    def before_request(self, request):
        # 处理请求开始之前的内容
        pass

    def after_request(self, req, resp):
        # 处理请求结束之后的内容
        pass
        
    def recv_data(self, request):
        """接受所有数据"""
        data = b""
        buffer_size = 1024
        flag = False
        while True:
            if flag:
                break
            d = request.recv(buffer_size)
            if len(d) < buffer_size:
                flag = True
            data += d
        return data
    
    def _response(self, response):
        if isinstance(response, HTTPResponse):
            response = str(response)
        return response

    def handle(self, request, _):
        data = self.recv_data(request)
        req = Request(data)
        response = self.before_request(req)
        if response is not None:
            return self._response(response)
        response = self.handle_request(req)
        if response is None:
            raise Exception("返回的响应不能为空")
        resp = self.after_request(req, response)
        if resp is not None:
            return self._response(resp)
        return self._response(response)
