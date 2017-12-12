import socketserver
from core import server_data_process

host = 'localhost'
port = 8009


class FtpServer(socketserver.BaseRequestHandler):

    def handle(self):
        conn = self.request
        conn.sendall("This is server...")
        print(conn.getpeername())
        instance_process = server_data_process.ServerDataProcess()
        flag = True
        while flag:
            data = conn.recv(8*1024)
            if not data:
                print("client broke")
                break
            instance_process.analyse_client_data(data)


def run():
    server = socketserver.ThreadingTCPServer((host, port), FtpServer)
    server.serve_forever()
