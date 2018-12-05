#!usr/bin/env python
# -*- coding:utf-8 -*-
# auther:Tony Cheung
# 描述：window 环境下测试通过.
import socket

MAX_LENGTH = 5*1024


class Client(object):
    """FTP 客户端类主要处理网络数据传输"""
    def __init__(self, host, port):
        self.host = host
        self.port = port
        """创建一个socket"""
        try:
            # print("new socket...")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.host, self.port))
            self.conn = s
        except ConnectionError as ex:
            print(ex)

    def get_response(self):
        """客户端接收服务器应答"""
        data = self.conn.recv(MAX_LENGTH)
        return data

    def send_request(self, args):
        """客户端请求服务器"""
        self.conn.sendall(str(args).encode("utf-8"))

    def send_request_length(self, args):
        """客户端请求数据长度"""
        self.conn.sendall(str(len(str(args))).encode("utf-8"))

    def close_socket(self):
        """关闭socket连接"""
        self.conn.close()

