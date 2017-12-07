import socket
from core import admin_role
from core import real_role
from core import guest_role


class Client(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = None
        self.login_statue = 0
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
                    if client.get_login_statue() == 1:
                        if recv_data.get("cmd") == "view" and recv_data.get("data") is not None:
                            # 这里解析出初始默认返回登陆访问到目录及目录中的文件
                            pass
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
