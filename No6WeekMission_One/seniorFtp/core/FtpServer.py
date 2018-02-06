import gevent
import socket
from gevent import socket, monkey
from conf import settings
from core import DataCenter
monkey.patch_all()


class FtpServer(object):
    """FTP 服务器类主要处理网络数据传输"""
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def server_init(self):
        """服务器初始化"""
        s = socket.socket()
        s.bind((self.host, self.port))
        s.listen(5)
        print("init server success")
        while True:
            cli, addr = s.accept()
            gevent.spawn(self.handle_request, cli)

    def handle_request(self, conn):
        """处理连接实例请求"""
        res_return_size = conn.recv(settings.size_control.get("level1"))
        if not res_return_size:
            conn.shutdown(socket.SHUT_WR)
        total_rece_size = int(res_return_size)
        conn.send("server ready,go ahead!".encode("utf-8"))
        received_size = 0
        res_data = b''
        while received_size != total_rece_size:
            data = conn.recv(settings.size_control.get("level5"))
            if not data:
                conn.shutdown(socket.SHUT_WR)
            received_size += len(data.decode())
            res_data += data
            print("received_size is:", received_size)
            print("total_rece_size is:", total_rece_size)
            if received_size == total_rece_size:
                dc = DataCenter(conn, res_data)
                dc.analyse_client_data()
                send_data = str(instance_process.get_process_res_data())
                try:
                    print("server send length is:", len(send_data))
                    conn.send(str(len(send_data)).encode(
                        "utf-8"))  # 发送之前先告诉客户端要发送多少数据给它,这里确实少不了,最开始没有这样做,发现客户端实际接收到的数据总是比服务端实际发的要小
                except Exception as e:
                    print("异常了:")
                    print(e)
                client_final_ack = conn.recv(settings.size_control.get("level1"))  # 等待客户端响应
                print("client response:", client_final_ack.decode())
                try:
                    print("server send: ", send_data)
                    conn.sendall(send_data.encode("utf-8"))
                except Exception as e:
                    print("异常错误信息:")
                    print(e)




