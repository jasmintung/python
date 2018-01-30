import os
import threading
from core import RoleBase
protocol = {"account": "", "password": "", "cmd": "", "data": ""}


class User(RoleBase):
    """普通用户类"""

    def __init__(self, conn):
        super(User, self).__init__(conn)
        self.conn = conn
        self.dir_files = ""
        self.upload_file_path = ""  # 待上传文件的绝对路径
        self.upload_file_size = 0  # 上传文件的总大小
        self.upload_file_offset = 0  # 已上传文件的大小
        self.download_file_path = ""
        self.upload_files_list = {}  # 待上传个文件的绝对路径字典
        self.download_files_list = []

    def set_default_home_path(self, args):
        """设置用户默认home路径"""
        User.home_dir = args

    def get_default_home_path(self):
        """获取用户默认home路径"""
        return User.home_dir

    def set_dir_files(self, args):
        """保存当前路径下的所有子目录及文件名"""
        self.dir_files = args

    def get_dir_files(self):
        """获取当前路径下的所有子目录及文件名"""
        return self.dir_files

    def login_result(self, value):
        home_dir = ""
        files_list = ""
        if len(value) > 1:
            is_login_statue, home_dir, files_list = value.strip().split("*")
        else:
            is_login_statue = value
        if is_login_statue == '1':
            print("\033[32;1m登陆成功\033[0m")
            self.update_login_statue(True)
            self.set_default_home_path(home_dir)
            self.set_dir_files(",".join(files_list.split("&")))
        elif is_login_statue == '0':
            print("\033[35;1m账户不存在!\033[0m")
            self.update_login_statue(False)
        elif is_login_statue == '9':
            print("\033[35;1m账户异常,无法登录,请联系管理员!\033[0m")
            self.update_login_statue(False)
        elif is_login_statue == '2':
            print("\033[35;1m用户名或密码错误!\033[0m")
        return is_login_statue, home_dir, files_list

    def process_server_response(self, args):
        """处理流程自动选择进行"""
        cmd = args.get("cmd")
        if cmd is not None:
            User.func_dict[cmd](args.get("data"))

    def view_files_request(self):
        """访问目录"""
        view_path = input("请输入访问目录或文件夹的绝对路径:").strip()
        protocol["account"] = RoleBase.account_id
        protocol["password"] = RoleBase.account_pwd
        protocol["cmd"] = "view"
        protocol["data"] = view_path
        # self.conn.send_request(protocol)

    def view_files_response(self, args):
        """访问目录服务器应答数据处理"""
        if args is not None:
            if args.startswith("no_permission"):
                print("\33[33;1m没有权限访问!\33[0m")
            elif args.startswith("path_error"):
                print("\33[33;1m路径错误!\33[0m")
            else:
                path, file_list = args.strip().split("*")
                print(path)
                print(" ".join(file_list.split("&")))
        else:
            print("服务器没有响应!")

    def upload_file_request(self, conn):
        """单任务上传请求"""
        upload_file_path = input("请输入要上传文件的绝对路径:").strip()
        if os.path.exists(upload_file_path):
            if os.path.isfile(upload_file_path):
                self.upload_file_path = upload_file_path
                self.upload_file_size = os.path.getsize(upload_file_path)
                file_name = ""
                remote_file_save_path = input("请输入服务器存储上传文件的目录路径:").strip()
                if remote_file_save_path.startswith(RoleBase.home_dir):
                    protocol["account"] = RoleBase.account_id
                    protocol["password"] = RoleBase.account_pwd
                    protocol["cmd"] = "upload"
                    protocol["data"] = remote_file_save_path + "*" + file_name + "*" + str(self.upload_file_size)
                    conn.tell_server_length(protocol)
                    return True
                else:
                    print("服务器存储路径错误")
            else:
                print("不是一个文件")
        else:
            print("上传文件的路径不存在")
        return False

    def upload_file_response(self, args):
        """单任务上传请求服务器应答数据处理"""
        if args.startswith("READY"):
            """可以开启线程开始上传文件了"""
            self.thread_upload_file(None)
        else:
            print("暂时无法上传文件")

    def download_file_request(self, conn):
        """单任务下载"""
        download_file_path = input("请输入要下载文件的绝对路径:").strip()
        if download_file_path.startswith(RoleBase.home_dir):  # 路径是否正确
            protocol["account"] = RoleBase.account_id
            protocol["password"] = RoleBase.account_pwd
            protocol["cmd"] = "download"
            protocol["data"] = download_file_path
            conn.send_request(protocol)
            return True
        else:
            print("输入下载路径有误")
        return False

    def download_file_response(self, args):
        """单任务下载请求服务器应答数据处理"""
        pass

    def upload_multi_files(self):
        """多任务上传"""
        pass

    def download_multi_files(self):
        """多任务下载"""
        pass

    def resume_tasks(self):
        """断点续传"""
        pass

    def deal_server_response_datas(self, conn):
        running_flag = True
        while running_flag:
            server_final_ack = conn.get_response()
            if not server_final_ack:
                continue
            total_rece_size = int(server_final_ack)  # 要接收的应答数据的大小
            conn.send_request(total_rece_size)  # 返回告知服务器知道即将接收的数据大小了
            received_size = 0
            res_data = b''

            while received_size != total_rece_size:
                cmd_res = conn.get_response()
                if not cmd_res:
                    continue
                received_size += len(cmd_res.decode())
                res_data += cmd_res

                if received_size == total_rece_size:

                    response_protocol = eval(str(server_final_ack.decode()))
                    print("server response:", response_protocol)
                    self.process_server_response(response_protocol)
                    cmd = response_protocol.get("cmd")
                    # if cmd == "login":
                    #     self.login_result(response_protocol.get("data"))
                    # elif cmd == "uploading":
                    #     self.thread_upload_file(response_protocol.get("data"))
                    # elif cmd == "download":
                    #     pass
                    # elif cmd == "upload":
                    #     self.upload_file_response(response_protocol.get("data"))
                    # elif cmd == "view":
                    #     self.view_files_response(response_protocol.get("data"))

    def thread_upload_file(self, conn, *args):
        """
        单个文件上传处理
        :param args: 上传文件的路径
        :return:
        """
        offset = 0
        if not args:
            pass
        else:
            result, server_file_length = args[0].strip().split("*")
            if result == "SUCCESS":
                self.upload_file_offset = offset
                print("上传文件的总大小:", self.upload_file_size)
                if int(server_file_length) == self.upload_file_size:
                    print("\033[33;1m上传完成\033[0m")
                    return 1
                else:
                    print("累计上传的文件大小:", int(server_file_length))
                    offset = int(server_file_length)
                    uf = open(self.upload_file_path, "rb")
                    if uf.readable():
                        response_protocol = {}
                        uf.seek(offset, 0)
                        protocol["account"] = RoleBase.account_id
                        protocol["password"] = RoleBase.account_pwd
                        protocol["cmd"] = "uploading"
                        protocol["data"] = uf.read(2 * 1024)  # 一次读2K
                        conn.tell_server_length(protocol)
                    uf.close()
            else:
                print("接收错误")

    func_dict = {"login": login_result, "view": view_files_response, "upload": upload_file_response, "uploading": thread_upload_file, "download": download_file_response}