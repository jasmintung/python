import gevent
import socket
import time
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
        print("来了一个连接...")
        dc = DataCenter.DataCenter(conn)
        while True:
            print("等待客户端数据...")
            res_return_size = conn.recv(settings.size_control.get("level1"))
            if not res_return_size:
                # conn.shutdown(socket.SHUT_WR)
                time.sleep(1000)
                continue
            total_rece_size = int(res_return_size)
            print("接收到客户端请求长度,应答客户端:", total_rece_size)
            conn.send("应答客户端请求长度".encode("utf-8"))
            received_size = 0
            res_data = b''
            while received_size != total_rece_size:
                data = conn.recv(settings.size_control.get("level5"))
                if not data:
                    # conn.shutdown(socket.SHUT_WR)
                    time.sleep(1000)
                    continue
                received_size += len(data.decode())
                res_data += data
                print("received_size is:", received_size)
                print("total_rece_size is:", total_rece_size)
                if received_size == total_rece_size:
                    print("接收客户端请求数据完成")
                    dc.analyse_client_data(res_data)
                    send_data = str(dc.get_response_data())
                    try:
                        print("应答数据长度:", len(send_data))
                        conn.send(str(len(send_data)).encode(
                            "utf-8"))  # 发送之前先告诉客户端要发送多少数据给它,这里确实少不了,最开始没有这样做,发现客户端实际接收到的数据总是比服务端实际发的要小
                    except Exception as e:
                        print("异常了:")
                        print(e)
                    client_final_ack = conn.recv(settings.size_control.get("level1"))  # 等待客户端响应
                    print("接收客户端长度应答:", client_final_ack.decode())
                    try:
                        print("开始发数据给客户端: ", send_data)
                        conn.sendall(send_data.encode("utf-8"))
                    except Exception as e:
                        print("异常错误信息:")
                        print(e)




