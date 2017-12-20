import socketserver
from core import server_data_process

host = 'localhost'
port = 9986


class FtpServer(socketserver.BaseRequestHandler):

    def handle(self):
        conn = self.request
        conn.sendall("This is server...".encode("utf-8"))
        print(conn.getpeername())
        instance_process = server_data_process.ServerDataProcess(conn)
        flag = True
        while flag:
            data = conn.recv(8*1024)
            if not data:
                print("client broke")
                break
            instance_process.analyse_client_data(data)
            send_data = str(instance_process.get_process_res_data())
            print("server send: ", send_data)
            conn.sendall(send_data.encode("utf-8"))


def run():
    server = socketserver.ThreadingTCPServer((host, port), FtpServer)
    server.serve_forever()
