import socket

def run():
    server = socket.socket()
    server.bind(('localhost', 6969))
    server.listen()

    while True:
        conn, addr = server.accept()
        print(conn, addr)
        while True:
            recv_datas = conn.recv(1024)
            if not recv_datas:
                print("recv datas null!")
                break
            conn.send(recv_datas.encode("utf-8"))
