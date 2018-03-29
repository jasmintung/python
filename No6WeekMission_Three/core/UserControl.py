#!usr/bin/env python
# -*- coding:utf-8 -*-
# auther:Tony Cheung
# 描述：window 环境下测试通过.
import os
import sys
import time
import threading
from core import Client
MAX_REQUEST_DOWN_SIZE = 5*1024
MAX_REQUEST_UPLOAD_SIZE = 5*1204

protocol_up = {"account": "", "password": "", "cmd": "", "data": {"head": "", "content": ""}}


def process_bar(type, current, total):
    process_type = ""
    if type == 0:
        process_type = "下载"
    elif type == 1:
        process_type = "上传"
    sys.stdout.write('\r')
    sys.stdout.write("%s进度:[%s]" % (process_type, int(current*100 / total)))
    sys.stdout.flush()
    time.sleep(0.5)
    if current == total:
        sys.stdout.write('\n')


def make_dir(path):
    """递归创建目录"""
    # print("ready to create path:", path)
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


class UserControl(object):

    def __init__(self, host, socket):
        self.host = host
        self.socket = socket

    protocol = ("account", "password", "cmd", "data")

    def downloading(self, conn, local_path, remote_path, current_size):
        """

        :param conn: socket
        :param local_path: 本地存储路径
        :param remote_path: 服务器获取地址
        :param current_size: 下载前本地已经下载的文件大小
        :return:
        """
        flag = True
        file_size = 0
        while flag:
            request_data = remote_path + "*" + str(current_size) + "*" + str(MAX_REQUEST_DOWN_SIZE)
            rs_data = dict(zip(UserControl.protocol, ("", "", "download", request_data)))
            conn.send_request_length(rs_data)  # 先告诉将要发送数据的长度
            conn.get_response()  # 等待响应
            conn.send_request(rs_data)  # 发送数据
            running_flag = True
            while running_flag:
                server_final_ack = conn.get_response()
                if not server_final_ack:
                    continue
                total_rece_size = int(server_final_ack)  # 要接收的应答数据的大小
                # print("接收服务器应答数据长度", total_rece_size)
                conn.send_request_length(total_rece_size)  # 返回告知服务器知道即将接收的数据大小了
                received_size = 0
                res_data = b''
                while received_size != total_rece_size:
                    cmd_res = conn.get_response()
                    if not cmd_res:
                        continue
                    received_size += len(cmd_res.decode())
                    res_data += cmd_res
                    if received_size == total_rece_size:
                        response_protocol = eval(str(res_data.decode()))
                        if isinstance(response_protocol, dict):
                            if response_protocol.get("data"):
                                write_data_head = response_protocol["data"]["head"]  # 文件总大小
                                file_size = int(write_data_head)
                                # print(current_size, file_size)
                                process_bar(0, current_size, file_size)
                                if current_size == file_size:
                                    print("\033[31;1m下载完成\033[0m")
                                    # sys.stdout.write('\n')
                                    running_flag = False
                                    flag = False
                                else:
                                    write_data_content = response_protocol["data"]["content"]  # 下载文件数据
                                    with open(local_path, "ab") as f:
                                        current_size += len(write_data_content)
                                        f.write(write_data_content)
                                    running_flag = False
                            else:
                                print("111数据有误")
                                running_flag = False
                                flag = False
                        else:
                            print("222数据有误")
                            running_flag = False
                            flag = False

    def download(self):
        """
        :param args: 文件地址*请求读位置*请求下载大小
        :return:
        """
        remote_path = input("请输入要下载文件的路径:")
        local_path = input("请输入下载文件本地存储路径:")
        current_size = 0
        if os.path.exists(local_path):
            if os.path.isfile(local_path):
                current_size = os.path.getsize(local_path)
            else:
                print("不是一个文件")
        else:
            dirs = local_path.split("\\")
            file_name = dirs[len(dirs) - 1]
            file_dir = local_path[0:local_path.find(file_name)]
            if make_dir(file_dir) is True:
                with open(local_path, "wb") as f:
                    pass
        client_instance = Client.Client(self.host, self.socket)  # 实例化socket
        t = threading.Thread(target=self.downloading, args=(client_instance, local_path, remote_path, current_size, ))
        t.setDaemon(True)
        t.start()

    def uploading(self, conn, local_path, remote_path, file_size):
        flag = True
        remote_size = 0
        while flag:
            if remote_size == file_size:
                print("\033[31;1m上传完成!\033[0m")
                # sys.stdout.write('\n')
                flag = False
            file_data = ""
            with open(local_path, "rb") as f:
                f.seek(remote_size)
                file_data = f.read(MAX_REQUEST_UPLOAD_SIZE)
            request_data = remote_path + "*" + str(remote_size) + "*" + str(file_size)
            protocol_up["account"] = ""
            protocol_up["password"] = ""
            protocol_up["cmd"] = "upload"
            protocol_up["data"]["head"] = request_data
            protocol_up["data"]["content"] = file_data
            conn.send_request_length(protocol_up)  # 先告诉将要发送数据的长度
            conn.get_response()  # 等待响应
            conn.send_request(protocol_up)  # 发送数据
            running_flag = True
            while running_flag:
                server_final_ack = conn.get_response()
                if not server_final_ack:
                    continue
                total_rece_size = int(server_final_ack)  # 要接收的应答数据的大小
                conn.send_request_length(total_rece_size)  # 返回告知服务器知道即将接收的数据大小了
                received_size = 0
                res_data = b''
                while received_size != total_rece_size:
                    cmd_res = conn.get_response()
                    if not cmd_res:
                        continue
                    received_size += len(cmd_res.decode())
                    res_data += cmd_res
                    if received_size == total_rece_size:
                        response_protocol = eval(str(res_data.decode()))
                        if isinstance(response_protocol, dict):
                            if response_protocol.get("data"):
                                data = response_protocol.get("data")
                                # print("client recv data:", data)
                                if isinstance(data, int):
                                    running_flag = False
                                    remote_size = data
                                    process_bar(1, remote_size, file_size)
                                elif isinstance(data, str):
                                    flag = False
                                    running_flag = False
                                    conn.close_socket()
                                    break
                                else:
                                    print("not known type")
                            else:
                                print("数据有误")
                                flag = False
                                running_flag = False
                                conn.close_socket()

                        else:
                            print("数据有误")
                            flag = False
                            running_flag = False
                            conn.close_socket()

    def upload(self):
        """
        :param args: data["head"]:文件存储地址*请求写位置*请求写总大小 data["content"]: 文件内容
        :return:
        """
        local_path = input("请选择要上传的文件,输入本地地址:")
        remote_path = input("请输入远程存储路径:")
        if os.path.exists(local_path):
            if os.path.isfile(local_path):
                file_size = os.path.getsize(local_path)
                client_instance = Client.Client(self.host, self.socket)  # 实例化socket
                t = threading.Thread(target=self.uploading, args=(client_instance, local_path, remote_path, file_size, ))
                t.setDaemon(True)
                t.start()
