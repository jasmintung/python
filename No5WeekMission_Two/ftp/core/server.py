import socketserver
from core import server_data_process

host = 'localhost'
port = 8009


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
                print("111 received_size is:", received_size)
                print("111 total_rece_size is:", total_rece_size)
                if received_size == total_rece_size:
                    instance_process.analyse_client_data(res_data)
                    send_data = str(instance_process.get_process_res_data())
                    print("server send length is:", len(send_data))
                    print("server send: ", send_data)
                    try:
                        conn.send(str(len(send_data)).encode("utf-8"))  # 发送之前先告诉客户端要发送多少数据给它,这里确实少不了,最开始没有这样做,发现客户端实际接收到的数据总是比服务端实际发的要小
                    except Exception as e:
                        print("异常了:")
                        print(e)
                    client_final_ack = conn.recv(1024)  # 等待客户端响应
                    print("客户端应答:", client_final_ack.decode())
                    try:
                        conn.sendall(send_data.encode("utf-8"))
                    except Exception as e:
                        print("异常错误信息:")
                        print(e)


def run():
    server = socketserver.ThreadingTCPServer((host, port), FtpServer)
    server.serve_forever()
