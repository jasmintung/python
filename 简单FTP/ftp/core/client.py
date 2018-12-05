import socket
import os,sys
from core import admin_role
from core import real_role
from core import guest_role
from conf import settings
# operation_fun = {0: "login", 1: "view", 2: "jump", 3: "download", 4: "upload"}
# download_file_save_base_path = "C:\\Users\Public"  # 下载文件存放在本地的根路径


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
        self.download_count_size = 0    # 单次任务累计收到的文件大小
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
        self.socket.settimeout(5*1000)  # 5秒的连接超时
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

    def set_download_count_size(self, args):
        self.download_count_size = args

    def get_download_count_size(self):
        return self.download_count_size


def run():
    while True:
        ip = input("请输入IP地址: ").strip()
        port = int(input("请输入端口: ").strip())
        client = Client(ip, port)
        result = client.init_socket()
        if result == 0:
            # client.get_socket().bind(("127.0.0.1", 9986))
            while True:
                data = client.get_socket().recv(1024)
                print("client recv data:", data.decode())
                if data:
                    break
            print("ftp server name is:", client.get_socket().getpeername())
            user_name = input("请输入登陆名:").strip()
            password = input("请输入登陆密码:").strip()
            login_protocol = {}
            login_protocol["account"] = user_name
            login_protocol["password"] = password
            login_protocol["cmd"] = "login"
            client.set_protocol(login_protocol)
            send_interface(client, login_protocol)
            # 这里要加--------------------
            # client.get_socket().send(str(len(str(login_protocol))).encode("utf-8"))
            # server_final_ack = client.get_socket().recv(1024)  # 等待客户端响应
            # print("server response:", server_final_ack.decode())
            # client.get_socket().sendall(str(login_protocol).encode("utf-8"))
            while True:
                res_return_size = client.get_socket().recv(1024)
                if not res_return_size:
                    continue
                print("client 接收到数据")
                total_rece_size = int(res_return_size)
                client.get_socket().send("client ready,go ahead!".encode("utf-8"))
                received_size = 0
                res_data = b''
                print("totalsize is:", total_rece_size)
                while received_size != total_rece_size:
                    cmd_res = client.get_socket().recv(10 * 1024)
                    if not cmd_res:
                        continue
                    received_size += len(cmd_res.decode())
                    res_data += cmd_res
                    print("client revc len: ", received_size)
                    print("recv data is :", cmd_res.decode())
                    if received_size == total_rece_size:
                        recv_data = eval(str(res_data.decode()))
                        if recv_data.get("account") == user_name and recv_data.get("password") == password:
                            if client.get_login_statue() == 0:
                                if recv_data.get("cmd") == "login":
                                    func_dict.get(recv_data.get("cmd"))(client, user_name,
                                                                        password, recv_data.get("data"))
                            elif client.get_login_statue() == 1:
                                if recv_data.get("cmd") == "view" or recv_data.get("cmd") == "jump":
                                    func_dict.get(recv_data.get("cmd"))(recv_data.get("cmd"), client,
                                                                        user_name, password,
                                                                        recv_data.get("data"))
                                else:
                                    func_dict.get(recv_data.get("cmd"))(client, user_name,
                                                                        password,
                                                                        recv_data.get("data"))
                        else:
                            print("账户不对!")
                            # print("接收错误! error code is %d" % result)
                            # client.get_socket().send("error receive".encode("utf-8"))
        else:
            # 这里要加--------------------
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


def process_login(client, account, password, args):
    print("登陆成功!")
    client.set_login_statue(1)
    instance_role = init_role(args, account, password)
    client.set_role_instance(instance_role)
    init_operation_protocol = {}
    init_operation_protocol["account"] = instance_role.get_user_name()
    init_operation_protocol["password"] = instance_role.get_password()
    init_operation_protocol["cmd"] = "view"
    init_operation_protocol["data"] = ""
    client.set_protocol(init_operation_protocol)
    send_interface(client, init_operation_protocol)


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
            print("目录中的文件及子目录有:")
            print(", ".join(file_list.split("&")))
        if client.get_role_instance().get_authority_level() == 9:
            admin_notice = """
                "创建用户": 1
                "删除用户": 0
                "其它操作": 任意输入
            """
            print(admin_notice)
            choice = (input("请根据编号选择操作:"))
            if choice == "0":
                print("\033[33;1m暂不支持\033[0m")
            elif choice == "1":
                print("\033[33;1m暂不支持\033[0m")
            else:
                process_view_func(client, account, password)
        else:
            process_view_func(client, account, password)


def process_view_func(client, account, password):
    notice_info = """
                    "目录跳转请输入: jump*具体你要跳转到的绝对路径名"
                    "上传文件请输入: upload*FTP服务器上您home目录下或者子目录下*本地要上传文件的绝对路径"
                    "下载文件请输入: download*服务器存放下载文件的绝对路径"
                    "退出": quit
                """
    print(notice_info)
    operation = input("请输入>>").strip()
    if operation == "quit":  # 退出
        client.close()
        exit()

    operation_protocol = {}
    operation_protocol["account"] = account
    operation_protocol["password"] = password
    if operation.startswith("upload"):
        # 这里加一个正则表达式来判断输入格式的正确性
        cmd, path_server, path_local = operation.strip().split("*")
        print("cmd:", cmd)
        print("path_server:", path_server)
        print("path_local:", path_local)
        user_default_path = client.get_role_instance().get_default_path()
        if os.path.isfile(path_local):
            if not path_server.startswith(user_default_path):
                print("上传路径有误!")
            else:
                client.set_upload_file_path(path_local)
                file_length = os.path.getsize(path_local)
                client.set_upload_file_length(file_length)
                operation_protocol["data"] = path_server + "*" + \
                                             os.path.basename(path_local) + \
                                             "*" + str(file_length)
                operation_protocol["cmd"] = cmd
                client.set_protocol(operation_protocol)
                send_interface(client, operation_protocol)
        else:
            print("上传的文件不存在!")
            process_view_func(client, account, password)
    else:
        cmd, path = operation.strip().split("*")
        print("cmd: %s path: %s" % (cmd, path))
        operation_protocol["data"] = path
        operation_protocol["cmd"] = cmd
        if cmd == "download":
            dir, file_name = os.path.split(path)
            save_dir = settings.download_file_save_base_path + "\\" + account
            if os.path.isfile(save_dir + "\\" + file_name):
                print("\033[31;1m已经下载过了!\033[0m")
                process_view_func(client, account, password)
            else:
                client.set_download_file_name(file_name)
                client.set_protocol(operation_protocol)
                send_interface(client, operation_protocol)
        else:
            client.set_protocol(operation_protocol)
            send_interface(client, operation_protocol)


def process_download_res(client, account, password, args):
    """

    :param client:      客户端socket实例
    :param account:     当前账户名称
    :param password:    当前账户密码
    :param args:        下载文件前服务器发送的基本下载信息
    :return:
    """
    if args != "file_not_exists":
        print("\033[33;1m下载文件的总大小:\033[0m", args)
        operation_protocol = {}
        operation_protocol["account"] = account
        operation_protocol["password"] = password
        operation_protocol["cmd"] = "download_RES"
        operation_protocol["data"] = "READY" + "*" + str(0)
        save_dir = settings.LOCAL_DOWNLOAD_DRI.get(download_file_save_base_path) + "\\" + account
        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)
        client.set_download_file_save_dir(save_dir)
        client.set_protocol(operation_protocol)
        send_interface(client, operation_protocol)
        client.set_download_file_size(int(args))
    else:
        if args.isdigit():
            print("\033[33;1m要下载的文件是空的!\033[0m")
        else:
            print("\033[33;1m文件不存在\033[0m")
        process_view_func(client, account, password)


def process_download_ing(client, account, password, data):
    """
    下载文件，处理下载数据
    :param client:      客户端socket实例
    :param account:     当前账户名称
    :param password:    当前账户密码
    :param data:        数据
    :return:
    """
    count_size = client.get_download_count_size()
    print("data is :", data)
    print("count_size is :", count_size)

    current_get_server_data_size = len(data)
    down_file_name = client.get_download_file_name()
    save_file_path = client.get_download_file_save_dir() + "\\" + down_file_name
    tmp_save_file_path = client.get_download_file_save_dir() + "\\" + down_file_name + ".tmp"
    print("save_file_path is :", save_file_path)
    print("current_get_size is :", current_get_server_data_size)
    print("client.get_download_file_size() is :", client.get_download_file_size())
    if not os.path.isfile(save_file_path):
        if not os.path.isfile(tmp_save_file_path):
            print("第一次写")
            wf = open(tmp_save_file_path, "wb")
        else:
            print("追加写")
            wf = open(tmp_save_file_path, "ab")
        res = process_download_write_file(client, account, password, wf, int(count_size) + current_get_server_data_size,
                                          data)

        if res == 1:
            os.rename(tmp_save_file_path, save_file_path)
            process_view_func(client, account, password)
        else:
            print("下载进度: %2d%s" %
                  (
                    int(((int(count_size) + current_get_server_data_size) / client.get_download_file_size())*100),
                    "%100")
                  )
    else:
        print("\033[31;1m已经下载过了!\033[0m")
        process_view_func(client, account, password)


def process_download_write_file(client, account, password, fp, total_size, data):
    """
    下载文件功能，写文件
    :param client:      客户端socket实例
    :param account:     当前账户名称
    :param password:    当前账户密码
    :param fp:          存下载数据的文件指针
    :param total_size:  累计已经收到的数据量
    :param data:        数据
    :return:            传输结果0: 未完成 or 1: 完成
    """
    write_result = 0
    client.set_download_count_size(int(total_size))
    fp.write(data)
    fp.close()
    operation_protocol = {}
    operation_protocol["account"] = account
    operation_protocol["password"] = password
    if int(total_size) < client.get_download_file_size():
        operation_protocol["cmd"] = "download_RES"
        operation_protocol["data"] = "READY" + "*" + str(total_size)
        client.set_protocol(operation_protocol)
        send_interface(client, operation_protocol)
        write_result = 0
    else:
        print("\033[33;1m下载完成\033[0m")
        client.set_download_count_size(0)
        write_result = 1
    return write_result


def process_upload_res(client, account, password, args):
    """
    上传文件功能，上传前与服务器的握手指令
    :param client:      客户端socket实例
    :param account:     当前账户名称
    :param password:    当前账户密码
    :param args:        服务器是否准备好了及异常返回
    :return:
    """
    if args == "READY":
        upload_res_protocol = {}
        upload_res_protocol["account"] = account
        upload_res_protocol["password"] = password
        upload_res_protocol["cmd"] = "upload_RES"
        upload_res_protocol["data"] = "READY"
        client.set_protocol(upload_res_protocol)
        # 这里要加--------------------
        send_interface(client, upload_res_protocol)


def process_upload_ing(client, account, password, args):
    """
    上传文件功能，处理实际上传文件的数据
    :param client:      客户端socket实例
    :param account:     当前账户名称
    :param password:    当前账户密码
    :param args:        结果*服务器累计收到的文件大小
    :return:
    """
    result, server_file_length = args.strip().split("*")
    print("累计上传的文件大小:", int(server_file_length))
    print("上传文件的总大小:", client.get_upload_file_length())
    if result == "SUCCESS":
        if int(server_file_length) == client.get_upload_file_length():
            print("\033[33;1m上传完成\033[0m")
            process_view_func(client, account, password)
        else:
            client.set_upload_file_offset(server_file_length)
            upload_res_protocol = {}
            upload_res_protocol["account"] = account
            upload_res_protocol["password"] = password
            upload_res_protocol["cmd"] = "upload_ing"
            rf = open(client.get_upload_file_path(), "rb")
            if rf.readable():
                rf.seek(int(client.get_upload_file_offset()), 0)
                upload_res_protocol["data"] = rf.read(2 * 1024)
            client.set_protocol(upload_res_protocol)
            send_interface(client, upload_res_protocol)
            print("上传进度: %2d%s" %
                  (
                      int(((int(server_file_length)) / client.get_upload_file_length()) * 100),
                      "%100")
                  )
    elif result == "FAILE":
        print("\033[31;1m;上传出错\033[0m")
        process_view_func(client, account, password)

func_dict = {"login": process_login, "view": process_view, "jump": process_view, "download_RES": process_download_res,
             "download_ing": process_download_ing, "upload_RES": process_upload_res, "upload_ing": process_upload_ing}


def send_interface(client, data):
    client.get_socket().send(str(len(str(data))).encode("utf-8"))
    server_final_ack = client.get_socket().recv(1024)  # 等待客户端响应
    print("server response:", server_final_ack.decode())
    client.get_socket().sendall(str(data).encode("utf-8"))
