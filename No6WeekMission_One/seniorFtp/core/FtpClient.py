import socket
from conf import settings


class FtpClient(object):
    """FTP 客户端类主要处理网络数据传输"""
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.conn = None

    def client_init(self):
        """客户端初始化"""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        self.conn = s

    def request(self):
        """客户端接收服务器应答"""
        while True:
            msg = input("想给服务器说点什么:")
            self.conn.sendall(str(msg).encode("utf-8"))
            data = self.conn.recv(settings.size_control.get("level1"))
            print("recv datas:", data.decode())

    def close_socket(self):
        """关闭socket连接"""
        self.conn.close()

    def test_bingfa(self):
        """测试用:协程并发功能"""
        while True:
            self.conn.sendall(str(self.conn.getsockname()).encode("utf-8"))
            data = self.conn.recv(settings.size_control.get("level1"))
            print("recv datas:", data.decode())
