import socket
import typing

if typing.TYPE_CHECKING:
    from app import Minx


def run_server(
    host: str,
    port: int,
    app: "Minx",
):
    srv = make_server(host, port, app)
    srv.serve_forever()


def make_server(
    host: str,
    port: int,
    app: "Minx",
):
    return HTTPServer(host, port, app)


class HTTPServer:
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 5

    def __init__(
        self,
        host,
        port,
        app,
    ):
        self.app = app
        self.socket = socket.socket(self.address_family, self.socket_type)
        self.server_address = (host, port)
        try:
            self.server_bind()
            self.server_activate()
        except:
            self.server_close()
            raise

    def serve_forever(self):
        self.__shutdown_request = False
        try:
            while not self.__shutdown_request:
                self._handle_request()
        except KeyboardInterrupt:
            pass
        finally:
            self.server_close()
    
    def _handle_request(self):
        try:
            request, addr = self.get_request()
            self.process_request(request, addr)
        except:
            self.shutdown_request(request)
            raise
    
    def process_request(self, request, addr):
        try:
            response = self.app.handle(request, addr)
            if response:
                request.send(response.encode())
        except:
            self.shutdown_request(request)
            raise

    def get_request(self):
        """ 获取客户端连接和客户端地址
        """
        return self.socket.accept()
    
    def server_close(self):
        self.socket.close()
    
    def server_bind(self):
        self.socket.bind(self.server_address)
        self.server_address = self.socket.getsockname()
    
    def server_activate(self):
        self.socket.listen(self.request_queue_size)
    
    def shutdown_request(self, request):
        request.close()
