import socketserver

host = 'localhost'
port = 8009


class FtpServer(socketserver.BaseRequestHandler):

    def handle(self):
        conn = self.request
        conn.sendall("This is server...")
        print(conn.getpeername())
        flag = True
        while flag:
            data = conn.recv(1024)
            if not data:
                print("client broke")
                break
            print(data.decode())
            if data.decode() == 'exit':
                flag = False


def run():
    server = socketserver.ThreadingTCPServer((host, port), FtpServer)
    server.serve_forever()
