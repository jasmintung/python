import socket
import os,sys
from core import admin_role
from core import real_role
from core import guest_role

operation_fun = {0: "login", 1: "view", 2: "jump", 3: "download", 4: "upload"}
download_file_save_base_path = "C:\\Users\Public"  # 下载文件存放在本地的根路径


class Client(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = None
        self.role = None
        self.login_statue = 0
        self.download_file_name = ""
        self.download_file_save_dir = ""
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
        print("port:", self.port)
        address = "".join(self.ip)
        print("address:", address)
        return self.socket.connect_ex((address, self.port))

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

    def get_download_file_name(self):
        return self.download_file_name

    def set_download_file_name(self, name):
        self.download_file_name = name

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

    def set_download_file_save_dir(self, args):
        self.download_file_save_dir = args

    def get_download_file_save_dir(self):
        return self.download_file_save_dir


def run():
    while True:
        ip = input("请输入IP地址: ").strip()
        port = int(input("请输入端口: ").strip())
        client = Client(ip, port)
        result = client.init_socket()
        if result == 0:
            while True:
                data = client.get_socket().recv(1024)
                print("客户端收到的数据:", data.decode())
                if data:
                    break
            user_name = input("请输入登陆名:").strip()
            password = input("请输入登陆密码:").strip()
            login_protocol = {}
            login_protocol["account"] = user_name
            login_protocol["password"] = password
            login_protocol["cmd"] = "login"
            client.set_protocol(login_protocol)
            client.get_socket().send(str(client.get_protocol()).encode("utf-8"))
            while True:
                data = client.get_socket().recv(10*1024)
                if not data:
                    continue
                print("client recv data:", data.decode())
                if len(data.decode()) > 20:
                    recv_data = eval(data.decode())
                    if recv_data.get("account") == user_name and recv_data.get("password") == password:
                        if client.get_login_statue() == 0:
                            if recv_data.get("cmd") == "login":
                                print("登陆成功!")
                                client.set_login_statue(1)
                                instance_role = init_role(recv_data.get("data"), user_name, password)
                                client.set_role_instance(instance_role)
                                init_operation_protocol = {}
                                init_operation_protocol["account"] = instance_role.get_user_name()
                                init_operation_protocol["password"] = instance_role.get_password()
                                init_operation_protocol["cmd"] = "view"
                                init_operation_protocol["data"] = ""
                                client.set_protocol(init_operation_protocol)
                                client.get_socket().send(str(client.get_protocol()).encode("utf-8"))
                        elif client.get_login_statue() == 1:
                            if recv_data.get("cmd") == "view":
                                # 这里解析出初始默认返回登陆访问到目录及目录中的文件
                                process_view("view", client, user_name, password, recv_data.get("data"))
                            elif recv_data.get("cmd") == "jump":  # 接收next指令应答
                                process_view("jump", client, user_name, password, recv_data.get("data"))
                            elif recv_data.get("cmd") == "download_RES":  # 接收download_RES指令应答
                                process_download_res(client, user_name, password, recv_data.get("data"))
                            elif recv_data.get("cmd") == "download_ing":  # 接收download_ing指令应答
                                process_download_ing(client)
                            elif recv_data.get("cmd") == "upload_RES":  # 接收upload_RES指令应答
                                process_upload_res(client, user_name, password, recv_data.get("data"))
                            elif recv_data.get("cmd") == "upload_ing":
                                process_upload_ing(client, user_name, password, recv_data.get("data"))

                else:
                    print("接收错误! error code is %d" % result)
                    client.get_socket().send("error receive".encode("utf-8"))
        else:
            client.get_socket().send("error receive".encode("utf-8"))
            print("连接错误! error code is %d" % result)


def init_role(type, *args):
    instance_user = None
    if type == 1:
        print("您是Real用户!")
        instance_user = real_role.Real(args[0], args[1])
    elif type == 2:
        print("您是Guest用户!")
        instance_user = guest_role.Guest(args[0], args[1])
    elif type == 9:
        print("您是Admin用户!")
        instance_user = admin_role.Admin(args[0], args[1])
    else:
        print("您的访问权限可能未分配!请联系后台管理员!")
    if not instance_user:
        instance_user.set_authority_level(type)
    return instance_user


def create_role():
    """
    管理员功能 之 创建普通用户
    :return:
    """
    account = input("请输入创建用户用户名:")
    password = input("请输入创建用户密码:")
    type = input("请输入创建用户类型:")


def delete_role():
    """
    管理员功能 之 创建普通用户
    :return:
    """
    account = input("请输入要删除的账户用户名:")


def process_view(cmd, client, account, password, args):
    if args.startswith("no_permission"):
        print("\33[33;1m没有权限访问!\33[0m")
        process_view_func(client, account, password)
    elif args.startswith("path_error"):
        print("\33[33;1m路径错误!\33[0m")
        process_view_func(client, account, password)
    else:
        path, file_list = args.strip().split("*")
        if cmd == "view":
            print("您的home目录是:", path)
            client.get_role_instance().set_default_path(path)
        elif cmd == "jump":
            print("您当前浏览的目录是:", path)
        if len(file_list) < 3:
            print("子目录是空的!")
        else:
            print("\n目录中的文件及子目录有:", file_list)
        if client.get_role_instance().get_authority_level() == 9:
            admin_notice = """
                "创建用户": 1
                "删除用户": 0
                "其它操作": 任意输入
            """
            print(admin_notice)
            choice = (input("请根据编号选择操作:"))
            if choice == "0":
                delete_role()
            elif choice == "1":
                create_role()
            else:
                process_view_func(client, account, password)
        else:
            process_view_func(client, account, password)


def process_view_func(client, account, password):
    notice_info = """
                    "目录跳转请输入: jump*具体你要跳转到的绝对路径名"
                    "上传文件请输入: upload*FTP服务器上自己的目录下的路径*本地要上传文件的绝对路径"
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
            user_default_path = client.get_role_instance().get_default_path()
            if os.path.isfile(path_local):
                if not path_server.startwith(user_default_path):
                    print("上传路径有误!")
                else:
                    client.set_upload_file_path(path_local)
                    file_length = client.set_upload_file_length(os.path.getsize(path_local))
                    operation_protocol["data"] = path_server + "*" + os.path.basename(path_local) + "*" + file_length
                    operation_protocol["cmd"] = cmd
                    client.set_protocol(operation_protocol)
                    client.get_socket().send(str(client.get_protocol()).encode("utf-8"))
            else:
                print("上传的文件不存在!")
        else:
            cmd, path = operation.strip().split("*")
            print("cmd: %s path: %s" % (cmd, path))
            operation_protocol["data"] = path
            operation_protocol["cmd"] = cmd
            if cmd == "download":
                dir, file_name = os.path.split(path)
                client.set_download_file_name(file_name)
            client.set_protocol(operation_protocol)
            client.get_socket().send(str(client.get_protocol()).encode("utf-8"))


def process_download_res(client, account, password, args):
    if args != "file_not_exists":
        print("下载文件的总大小:", args)
        operation_protocol = {}
        operation_protocol["account"] = account
        operation_protocol["password"] = password
        operation_protocol["cmd"] = "download_RES"
        operation_protocol["data"] = "READY"
        save_dir = download_file_save_base_path + "\\" + account
        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)
        client.set_download_file_save_dir(save_dir)
        client.set_protocol(operation_protocol)
        client.get_socket().send(str(client.get_protocol()).encode("utf-8"))
        client.set_download_file_size(args)
    else:
        print("\033[33;1m文件不存在\033[0m")
        process_view_func(client, account, password)


def process_download_ing(client):
    current_get_size = 0
    file_datas = b''
    down_file_name = client.get_download_file_name()
    save_file_path = client.get_download_file_save_dir() + "\\" + down_file_name
    if not os.path.isfile(save_file_path):
        wf = open(save_file_path, "wb")
    else:
        wf = open(save_file_path, "ab")
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
        client.get_socket().send(str(client.get_protocol()).encode("utf-8"))


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
        client.get_socket().send(str(client.get_protocol()).encode("utf-8"))
