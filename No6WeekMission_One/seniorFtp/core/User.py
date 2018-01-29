import os
from core import RoleBase
protocol = {"account": "", "password": "", "cmd": "", "data": ""}


class User(RoleBase):
    """普通用户类"""

    def __init__(self, conn):
        super(User, self).__init__(conn)
        self.conn = conn
        self.upload_files_list = {}
        self.download_files_list = {}

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
        self.conn.send_request(protocol)

    def view_files_response(self, args):
        """访问目录服务器应答数据处理"""
        data = args.get("data")
        if data is not None:
            if data.startswith("no_permission"):
                print("\33[33;1m没有权限访问!\33[0m")
            elif data.startswith("path_error"):
                print("\33[33;1m路径错误!\33[0m")
            else:
                path, file_list = data.strip().split("*")
                print(path)
                print(" ".join(file_list.split("&")))
        else:
            print("服务器没有响应!")

    def upload_file_request(self):
        """单任务上传请求"""
        upload_file_path = input("请输入要上传文件的绝对路径:").strip()
        if os.path.exists(upload_file_path):
            if os.path.isfile(upload_file_path):
                file_name = ""
                remote_file_save_path = input("请输入服务器存储上传文件的目录路径:").strip()
                if remote_file_save_path.startswith(RoleBase.home_dir):
                    protocol["account"] = RoleBase.account_id
                    protocol["password"] = RoleBase.account_pwd
                    protocol["cmd"] = "upload"
                    protocol["data"] = remote_file_save_path + "*" + file_name + "*" + os.path.getsize(file_name)
                    self.conn.send_request(protocol)
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
        data = args.get("data")
        if data.startswith("READY"):
            """可以开启线程开始上传文件了"""
        else:
            print("暂时无法上传文件")

    def download_file_request(self):
        """单任务下载"""
        download_file_path = input("请输入要下载文件的绝对路径:").strip()
        if download_file_path.startswith(RoleBase.home_dir):  # 路径是否正确
            protocol["account"] = RoleBase.account_id
            protocol["password"] = RoleBase.account_pwd
            protocol["cmd"] = "download"
            protocol["data"] = download_file_path
            self.conn.send_request(protocol)
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

    func_dict = {"view": view_files_response, "upload": upload_file_response, "download": download_file_response}