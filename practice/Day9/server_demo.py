import gevent
import socket
from gevent import socket, monkey
monkey.patch_all()


def server():
    s = socket.socket()
    s.bind(('localhost', 9986))
    s.listen(500)
    while True:
        cli, addr = s.accept()
        gevent.spawn(handle_request, cli)


def handle_request(conn):
    try:
        while True:
            data = conn.recv(1024)
            print("recv:", data)
            conn.send(data)
            if not data:
                conn.shutdown(socket.SHUT_WR)

    except Exception as ex:
        print(ex)
    finally:
        conn.close()

if __name__ == "__main__":
    server()