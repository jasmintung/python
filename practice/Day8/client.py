import socket
import sys

HOST, PORT = "localhost", 9986
data = "".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall((bytes(data + "\n", "utf-8")))
    # Received data from the server and shut down
    received = str(sock.recv(1024), "utf-8")
finally:
    sock.close()
