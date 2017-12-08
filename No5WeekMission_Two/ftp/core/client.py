import socket
from core import admin_role
from core import real_role
from core import guest_role

operation_fun = {0: "login", 1: "view", 2: "next", 3: "prev", 4: "download", 5: "upload"}
download_file_save_path = ""  # 下载文件存放在本地的具体地址


class Client(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = None
        self.login_statue = 0
        self.download_file_size = 0
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
                data = client.get_socket().recv(1024)
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
                            process_view(client, user_name, password, recv_data.get("data"))
                        elif recv_data.get("cmd") == "next" and recv_data.get("data") is not None:  # 接收next指令应答
                            process_view(client, user_name, password, recv_data.get("data"))
                        elif recv_data.get("cmd") == "prev" and recv_data.get("data") is not None:  # 接收prev指令应答
                            process_view(client, user_name, password, recv_data.get("data"))
                        elif recv_data.get("cmd") == "download_RES" and recv_data.get("data") is not None:  # 接收download_RES指令应答
                            process_download_res(client, user_name, password, recv_data.get("data"))
                        elif recv_data.get("cmd") == "download_ing" and recv_data.get("data") is not None:  # 接收download_ing指令应答
                            process_download_ing()
                        elif recv_data.get("cmd") == "upload" and recv_data.get("data") is not None:  # 接收upload指令应答
                            process_upload()

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


def process_view(client, account, password, args):
    path, file_list = args.strip().split("*")
    print("当前目录是:", path)
    print(file_list)
    notice_info = """
        "目录向前跳转请输入: next*具体你要跳转到的路径地址"
        "目录向后跳转请输入: next*具体你要跳转到的路径地址"
        "上传文件请输入: upload*具体文件路径"
        "下载文件请输入: download*具体文件路径"
    """
    print(notice_info)
    operation = input("请输入>>").strip()
    check = False
    for key in operation_fun:
        if operation.startswith(operation_fun[key]):
            check = True
            break
    if check:
        cmd, path = operation.strip().split("*")
        operation_protocol = {}
        operation_protocol["account"] = account
        operation_protocol["password"] = password
        operation_protocol["cmd"] = cmd
        operation_protocol["data"] = path
        client.set_protocol(operation_protocol)


def process_next():
    pass


def process_prev():
    pass


def process_download():
    pass


def process_upload():
    pass


def process_download_res(client, account, password, args):
    print("下载文件的总大小:", args)
    operation_protocol = {}
    operation_protocol["account"] = account
    operation_protocol["password"] = password
    operation_protocol["cmd"] = "download_RES"
    operation_protocol["data"] = "READY"
    client.set_protocol(operation_protocol)
    client.set_download_file_size(args)


def process_download_ing(client, account, password, args):
    download_ing = True
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
