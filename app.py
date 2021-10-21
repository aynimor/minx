import socket


def response():
    return b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<h1>Hello World!</h1>"


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
        s.listen(1)
        while True:
            try:
                conn, addr = s.accept()
                print(addr)
                data = conn.recv(1024)
                print(data)
                conn.send(response())
            except KeyboardInterrupt:
                break
            finally:
                conn.close()

                
        s.close()

if __name__ == "__main__":
    main()
