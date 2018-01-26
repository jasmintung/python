import gevent
import socket
from gevent import socket, monkey
from conf import settings


class FtpServer(object):
    """FTP 服务器类主要处理网络数据传输"""
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def server_init(self):
        """服务器初始化"""
        s = socket.socket()
        s.bind((self.host, self.port))
        s.listen()
        print("init server success")
        while True:
            cli, addr = s.accept()
            gevent.spawn(self.handle_request, cli)

    def handle_request(self, conn):
        """处理连接实例请求"""
        try:
            while True:
                data = conn.recv(settings.size_control.get("level1"))
                print("recv datas:", data)
                if not data:
                    conn.shutdown(socket.SHUT_WR)
                else:
                    conn.send(data)
        except Exception as ex:
            print(ex)
        finally:
            conn.close()
