import socket
from core import admin_role
from core import real_role
from core import guest_role
protocol = {"account": "", "password": "", "cmd": "", "data": 0}


class Client(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = None

    def init_socket(self):
        self.socket = socket.socket()
        return self.socket.connect_ex((self.ip, self.port))

    def get_socket(self):
        return self.socket


def run():
    while True:
        ip = input("请输入IP地址: ").strip()
        port = input("请输入端口: ").strip()
        client = Client(ip, port)
        result = client.init_socket()
        if result == 0:
            user_name = input("请输入登陆名:").strip()
            password = input("请输入登陆密码:").strip()
            protocol["account"] = user_name
            protocol["password"] = password
            protocol["cmd"] = "login"
            while True:
                client.get_socket().send(str(protocol).encode("utf-8"))
                data = client.get_socket().recv(1024)
                if not data:
                    print("recv data is null!")
                    continue
                print("recv data is:", data.decode())
                recv_data = eval(data.decode())
                if recv_data.get("account") == user_name and recv_data.get("password") == password:
                    if recv_data.get("cmd") == "login" and recv_data.get("data") != 0:
                        print("登陆成功!")
                        instance_role = init_role(recv_data.get("data"), user_name, password)

        else:
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
    return instance_user
