import select
import socket
import sys
import queue

server = socket.socket()
server.setblocking(0)

server_addr = ('127.0.0.1', 9986)  # ip, 端口
server.bind(server_addr)  # 绑定ip,端口
server.listen(5)  # 监听个数

inputs = [server, ]  # 监测列表,以为server本身也是个fd
outputs = []

message_queues = {}

while True:
    print("waiting for next event...")
    # 如果没有任何IO就绪,程序会一直阻塞在这里
    readable, writeable, exceptional = select.select(inputs, outputs, inputs)
    for s in readable:  # 每个s就是一个socket
        if s is server:  # 如果s 是 server，代表server 这个fd就就绪了
            conn, client_addr = s.accept()
            print("new connection from", client_addr)
            conn.setblocking(0)
            inputs.append(conn)  # 为了不阻塞整个程序,我们不会立即在这里开始接收客户端发来的数据,把它放到inputs里,
            message_queues[conn] = queue.Queue()  # 接收到客户端的数据后,不立即返回,暂时存到队列里面,以后发送
        else:  # s 不是server的话,那就只能是一个与客户端建立的连接的fd了
            data = s.recv(1024)
            if data:
                print("收到来自[%s]的数据:" % s.getpeername()[0], data)
                message_queues[s].put(data)
                if s not in outputs:
                    outputs.append(s)
            else:
                print("客户端断开", s)
                if s in outputs:
                    outputs.remove(s)  # 清理已断开的连接
                inputs.remove(s)  # 清理已断开的连接
                del message_queues[s]   # 清理已断开的连接