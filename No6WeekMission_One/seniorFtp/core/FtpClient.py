import socket
from conf import settings


class FtpClient(object):
    """FTP 客户端类主要处理网络数据传输"""
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.conn = None

    def new_socket(self):
        """创建一个socket"""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        return s

    def request(self):

        while True:
            msg = input("想给服务器说点什么:")
            self.conn.sendall(str(msg).encode("utf-8"))
            data = self.conn.recv(settings.size_control.get("level1"))
            print("recv datas:", data.decode())

    def get_response(self):
        """客户端接收服务器应答"""
        data = self.conn.recv(settings.size_control.get("level1"))
        return data

    def send_request(self, args):
        """客户端请求服务器"""
        self.conn.sendall(str(args).encode("utf-8"))

    def send_request_length(self, args):
        """客户端请求数据长度"""
        self.conn.sendall(str(len(str(args))).encode("utf-8"))

    def close_socket(self):
        """关闭socket连接"""
        self.conn.close()

    def test_bingfa(self):
        """测试用:协程并发功能"""
        while True:
            self.conn.sendall(str(self.conn.getsockname()).encode("utf-8"))
            data = self.conn.recv(settings.size_control.get("level1"))
            print("recv datas:", data.decode())
