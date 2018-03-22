#!usr/bin/env python
# -*- coding:utf-8 -*-
import selectors
import socket
import time
import os

sel = selectors.DefaultSelector()
MAX_LENGTH = 10*1024
host = 'localhost'
port = 9986

protocol = {"account": "", "password": "", "cmd": "", "data": ""}
protocol_up = {"account": "", "password": "", "cmd": "", "data": {"head": "", "content": ""}}


def make_dir(path):
    """递归创建目录"""
    print("ready to create path:", path)
    if not os.path.isdir(path):
        make_dir(os.path.split(path)[0])
    else:
        return True
    try:
        os.mkdir(path)
    except NotImplementedError as e:
        print(e)
    finally:
        return True


def upload(args):
    """
    客户端上传请求
    :param args: data["head"]:文件存储地址*请求写位置*请求写总大小 data["content"]: 文件内容
    :return:已经写入的文件大小
    """
    if args.get("data"):
        file_head = args["data"]["head"]
        file_data = args["data"]["content"]
        file_path, offset, size = file_head.split("*")
        protocol["account"] = ""
        protocol["password"] = ""
        protocol["cmd"] = "upload"
        data = None
        if os.path.exists(file_path):
            already_file_size = os.path.getsize(file_path)
            if int(size) == already_file_size:
                print("文件已经存在!")
                data = "file already exists"
            else:
                print("持续上传文件!")
                try:
                    with open(file_path, "ab") as f:
                        offset = int(offset)
                        if offset == 0 and already_file_size != 0:
                            offset = already_file_size
                        f.seek(offset)
                        f.write(file_data)
                        data = int(offset) + len(file_data)
                except Exception as e:
                    data = str(e)
        else:
            dirs = file_path.split("\\")
            file_name = dirs[len(dirs) - 1]
            file_dir = file_path[0:file_path.find(file_name)]
            if make_dir(file_dir) is True:
                print("创建目录成功")
                with open(file_path, 'wb') as f:
                    offset = int(offset)
                    f.seek(offset)
                    f.write(file_data)
                    data = int(offset) + len(file_data)
            else:
                data = "path create error"
        protocol["data"] = data
        return protocol


def download(args):
    """
    客户端下载请求
    :param args: 文件地址*请求读位置*请求下载大小
    :return:head:剩余下载大小, content:当前下载数据
    """
    file_path, offset, size = args.get('data').split("*")
    if os.path.exists(file_path):
        if os.path.isfile(file_path):
            with open(file_path, "rb") as f:
                offset = int(offset)
                f.seek(offset)
                size = int(size)
                file_data = f.read(size)
                protocol_up["account"] = ""
                protocol_up["password"] = ""
                protocol_up["cmd"] = "download"
                protocol_up["data"]["head"] = os.path.getsize(file_path) - offset - len(file_data)
                protocol_up["data"]["content"] = file_data
                return protocol_up

ftp_func = {"upload": upload, "download": download}


def data_analyse(args):
    recv_data = eval(str(args.decode()))
    if isinstance(recv_data, dict):
        cmd = recv_data.get("cmd")
        print("cmd is :", cmd)
        return ftp_func.get(cmd)(recv_data)


def accept(sock, mask):
    conn, addr = sock.accept()
    print('accepted', conn, 'from', addr)
    # conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)


def read(conn, mask):
    data_length = conn.recv(MAX_LENGTH)
    if not data_length:
        pass
    else:
        total_size = int(data_length)
        conn.send("server received".encode("utf-8"))
        recv_length = 0  # 接收到的数据长度
        total_data = b''  # 累计接收到的数据
        while recv_length != total_size:
            recv_data = conn.recv(MAX_LENGTH)
            if not recv_data:
                time.sleep(0.5)
                continue
            recv_length += len(recv_data.decode())
            total_data += recv_data
            if recv_length == total_size:
                response_data = data_analyse(total_data)
                if isinstance(response_data, dict):
                    response_data = str(response_data)
                    print(response_data)
                    try:
                        conn.send(str(len(response_data)).encode(
                            "utf-8"))  # 发送之前先告诉客户端要发送多少数据给它,这里确实少不了,最开始没有这样做,发现客户端实际接收到的数据总是比服务端实际发的要小
                    except Exception as e:
                        print(e)
                    client_final_ack = conn.recv(MAX_LENGTH)  # 等待客户端响应
                    print("接收客户端长度应答:", client_final_ack.decode())
                    try:
                        print("开始发数据给客户端: ", response_data)
                        conn.sendall(response_data.encode("utf-8"))
                    except Exception as e:
                        print("异常错误信息:")
                        print(e)

        else:
            print('closing', conn)
            # sel.unregister(conn)
            # conn.close()


def main():
    sock = socket.socket()
    sock.bind((host, port))
    sock.listen(5000)
    # sock.setblocking(False)
    sel.register(sock, selectors.EVENT_READ, accept)

    while True:
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)
        time.sleep(0.2)
