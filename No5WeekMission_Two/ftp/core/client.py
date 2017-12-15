import socket
import os,sys
from core import admin_role
from core import real_role
from core import guest_role

operation_fun = {0: "login", 1: "view", 2: "jump", 3: "download", 4: "upload"}
download_file_save_path = ""  # 下载文件存放在本地的具体地址


class Client(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = None
        self.role = None
        self.login_statue = 0
        self.download_file_size = 0
        self.upload_file_path = ""
        self.upload_file_offset = 0  # 上传文件的偏移量
        self.upload_file_length = 0  # 上传文件总大小
        self.protocol = {
            "account": "",
            "password": "",
            "cmd": "",
            "data": 0}

    def init_socket(self):
        self.socket = socket.socket()
        return self.socket.connect_ex((self.ip, self.port))

    def get_socket(self):
        return self.socket

    def set_protocol(self, protocol):
        self.protocol = protocol

    def get_protocol(self):
        return self.protocol

    def set_login_statue(self, args):
        self.login_statue = args

    def get_login_statue(self):
        return self.login_statue

    def set_download_file_size(self, args):
        self.download_file_size = args

    def get_download_file_size(self):
        return self.download_file_size

    def set_upload_file_path(self, args):
        self.upload_file_path = args

    def get_upload_file_path(self):
        return self.upload_file_path

    def set_upload_file_offset(self, args):
        self.upload_file_offset = args

    def get_upload_file_offset(self):
        return self.upload_file_offset

    def set_upload_file_length(self, args):
        self.upload_file_length = args

    def get_upload_file_length(self):
        return self.upload_file_length

    def close(self):
        self.socket.close()

    def set_role_instance(self, role):
        self.role = role

    def get_role_instance(self):
        return self.role

def run():
    while True:
        ip = input("请输入IP地址: ").strip()
        port = input("请输入端口: ").strip()
        client = Client(ip, port)
        result = client.init_socket()
        if result == 0:
            user_name = input("请输入登陆名:").strip()
            password = input("请输入登陆密码:").strip()
            login_protocol = {}
            login_protocol["account"] = user_name
            login_protocol["password"] = password
            login_protocol["cmd"] = "login"
            client.set_protocol(login_protocol)
            while True:
                client.get_socket().send(str(client.get_protocol()).encode("utf-8"))
                data = client.get_socket().recv(10*1024)
                if not data:
                    print("recv data is null!")
                    continue
                print("recv data is:", data.decode())
                recv_data = eval(data.decode())
                if recv_data.get("account") == user_name and recv_data.get("password") == password:
                    if client.get_login_statue() == 0:
                        if recv_data.get("cmd") == "login" and recv_data.get("data") != 0:
                            print("登陆成功!")
                            client.set_login_statue(1)
                            instance_role = init_role(recv_data.get("data"), user_name, password)
                            init_operation_protocol = {}
                            init_operation_protocol["account"] = instance_role.get_user_name()
                            init_operation_protocol["password"] = instance_role.get_password()
                            init_operation_protocol["cmd"] = "view"
                            init_operation_protocol["data"] = ""
                            client.set_protocol(init_operation_protocol)
                    elif client.get_login_statue() == 1:
                        if recv_data.get("cmd") == "view" and recv_data.get("data") is not None:
                            # 这里解析出初始默认返回登陆访问到目录及目录中的文件
                            process_view("view", client, user_name, password, recv_data.get("data"))
                        elif recv_data.get("cmd") == "jump" and recv_data.get("data") is not None:  # 接收next指令应答
                            process_view("jump", client, user_name, password, recv_data.get("data"))
                        elif recv_data.get("cmd") == "download_RES" and recv_data.get("data") is not None:  # 接收download_RES指令应答
                            process_download_res(client, user_name, password, recv_data.get("data"))
                        elif recv_data.get("cmd") == "download_ing" and recv_data.get("data") is not None:  # 接收download_ing指令应答
                            process_download_ing(client)
                        elif recv_data.get("cmd") == "upload_RES" and recv_data.get("data") is not None:  # 接收upload_RES指令应答
                            process_upload_res(client, user_name, password, recv_data.get("data"))
                        elif recv_data.get("cmd") == "upload_ing" and recv_data.get("data") is not None:
                            process_upload_ing(client, user_name, password, recv_data.get("data"))
        else:
            print("连接错误! error code is %d" % result)


def init_role(type, *args):
    instance_user = None
    if type == 1:
        print("您是Real用户!")
        instance_user = real_role.Real(args[0], args[1], 1)
    elif type == 2:
        print("您是Guest用户!")
        instance_user = guest_role.Guest(args[0], args[1], 2)
    elif type == 9:
        print("您是Admin用户!")
        instance_user = admin_role.Admin(args[0], args[1], 9)
    else:
        print("您的访问权限可能未分配!请联系后台管理员!")
    return instance_user


def process_view(cmd, client, account, password, args):
    if args.startwith("no_permission"):
        print("\33[33;1m没有权限访问!\33[0m")
    elif args.startwith("path_error"):
        print("\33[33;1m路径错误!\33[0m")
    else:
        path, file_list = args.strip().split("*")
        if cmd == "view":

        print("当前目录是:", path)
        print("文件列表:", file_list)
        notice_info = """
            "目录跳转请输入: jump*具体你要跳转到的绝对路径名"
            "上传文件请输入: upload*服务器存放上传文件的绝对路径*本地要上传文件的绝对路径"
            "下载文件请输入: download*服务器存放下载文件的绝对路径"
            "退出": quit
        """
        print(notice_info)
        operation = input("请输入>>").strip()
        check = False
        if operation == "quit":  # 退出
            client.close()
            exit()
        for key in operation_fun:
            if operation.startswith(operation_fun[key]):
                check = True
                break
        if check:
            operation_protocol = {}
            operation_protocol["account"] = account
            operation_protocol["password"] = password
            if operation.startswith("upload"):
                cmd, path_server, path_local = operation.strip().split("*")
                if os.path.isfile(path_local):
                    operation_protocol["data"] = path_server +"*" + path_local
                    client.set_upload_file_path(path_local)
                    client.set_upload_file_length(os.path.getsize(path_local))
                    operation_protocol["cmd"] = cmd
                    client.set_protocol(operation_protocol)
                else:
                    print("上传的文件不存在!")
            else:
                cmd, path = operation.strip().split("*")
                operation_protocol["data"] = path
                operation_protocol["cmd"] = cmd
                client.set_protocol(operation_protocol)


def process_download_res(client, account, password, args):
    if args != "file_not_exists":
        print("下载文件的总大小:", args)
        operation_protocol = {}
        operation_protocol["account"] = account
        operation_protocol["password"] = password
        operation_protocol["cmd"] = "download_RES"
        operation_protocol["data"] = "READY"
        client.set_protocol(operation_protocol)
        client.set_download_file_size(args)
    else:
        pass


def process_download_ing(client):
    current_get_size = 0
    file_datas = b''
    wf = open(download_file_save_path, "wb")
    while current_get_size != client.get_download_file_size():
        data = client.get_socket().recv(4*1024)
        current_get_size += len(data)
        file_datas += data
    else:
        print("下载完成!")
        wf.write(file_datas)
        wf.close()


def process_upload_res(client, account, password, args):
    # 服务器 - -------------------------------------------->客户端
    # account = xxx
    # password = xxx
    # cmd = "upload_RES"
    # data = "READY" or "NOT_READY"
    if args == "READY":
        upload_res_protocol = {}
        upload_res_protocol["account"] = account
        upload_res_protocol["password"] = password
        upload_res_protocol["cmd"] = "upload_RES"
        upload_res_protocol["data"] = "READY"
        client.set_protocol(upload_res_protocol)

def process_upload_ing(client, account, password, args):
    # 服务器 - -------------------------------------------->客户端
    # account = xxx
    # password = xxx
    # cmd = "upload_ing"
    # data = 结果("SUCCESS") or "(FAILE)*累积收到的文件大小
    is_upload_end = False
    result, server_file_length = args.strip().split("*")
    if result == "SUCCESS":
        if server_file_length == client.get_upload_file_length():
            print("\033[33;1m上传完成\033[0m")
            is_upload_end = True
        else:
            client.set_upload_file_offset(server_file_length)
    elif result == "FAILE":
        pass
    if not is_upload_end:
        upload_res_protocol = {}
        upload_res_protocol["account"] = account
        upload_res_protocol["password"] = password
        upload_res_protocol["cmd"] = "upload_ing"
        rf = open(client.get_upload_file_path(), "rb")
        if rf.readable():
            rf.seek(client.get_upload_file_offset(), 0)
            upload_res_protocol["data"] = len(rf.read(2*1024))
        client.set_protocol(upload_res_protocol)