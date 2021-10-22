import socket
import json

from request import Request
from utils import log


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
