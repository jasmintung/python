import socketserver
from core import server_data_process
from conf import settings


class FtpServer(socketserver.BaseRequestHandler):

    def handle(self):
        conn = self.request
        conn.sendall("This is server...".encode("utf-8"))
        print(conn.getpeername())
        instance_process = server_data_process.ServerDataProcess(conn)
        flag = True

        while flag:
            res_return_size = conn.recv(8*1024)
            if not res_return_size:
                continue
            total_rece_size = int(res_return_size)
            conn.send("server ready,go ahead!".encode("utf-8"))
            received_size = 0
            res_data = b''
            while received_size != total_rece_size:
                data = conn.recv(8*1024)
                if not data:
                    continue
                received_size += len(data.decode())
                res_data += data
                print("received_size is:", received_size)
                print("total_rece_size is:", total_rece_size)
                if received_size == total_rece_size:
                    instance_process.analyse_client_data(res_data)
                    send_data = str(instance_process.get_process_res_data())
                    try:
                        print("server send length is:", len(send_data))
                        conn.send(str(len(send_data)).encode("utf-8"))  # 发送之前先告诉客户端要发送多少数据给它,这里确实少不了,最开始没有这样做,发现客户端实际接收到的数据总是比服务端实际发的要小
                    except Exception as e:
                        print("异常了:")
                        print(e)
                    client_final_ack = conn.recv(1024)  # 等待客户端响应
                    print("client response:", client_final_ack.decode())
                    try:
                        print("server send: ", send_data)
                        conn.sendall(send_data.encode("utf-8"))
                    except Exception as e:
                        print("异常错误信息:")
                        print(e)


def run():
    host = settings.SERVER_CONFIG.get("host")
    port = int(settings.SERVER_CONFIG.get("port"))
    # 这里可以加个正则校验来判断配置的合法性，时间原因后续完善，不影响本次作业功能，请手动配置的时候注意下。
    server = socketserver.ThreadingTCPServer((host, port), FtpServer)
    server.serve_forever()
