import os
import threading
from core import RoleBase
from conf import settings
protocol = {"account": "", "password": "", "cmd": "", "data": ""}


class User(RoleBase):
    """普通用户类"""
    is_login = False

    def __init__(self):
        super(User, self).__init__()
        self.view_path = ""
        self.dir_files = ""
        self.upload_file_path = ""  # 待上传文件的绝对路径
        self.upload_file_size = 0  # 上传文件的总大小
        self.upload_file_offset = 0  # 已上传文件的大小
        self.download_file_path = ""
        self.upload_files_list = {}  # 待上传个文件的绝对路径字典
        self.download_files_list = []

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
            self.set_cur_view_path(home_dir)
            self.set_dir_files(",".join(files_list.split("&")))
        elif is_login_statue == '0':
            print("\033[35;1m账户不存在!\033[0m")
            self.update_login_statue(False)
        elif is_login_statue == '9':
            print("\033[35;1m账户异常,无法登录,请联系管理员!\033[0m")
            self.update_login_statue(False)
        elif is_login_statue == '2':
            print("\033[35;1m用户名或密码错误!\033[0m")

    @staticmethod
    def process_server_response(data, conn, args):
        """处理流程自动选择进行"""
        cmd = data.get("cmd")
        if cmd is not None:
            User.func_dict[cmd](data.get("data"), conn, args)

    def view_files_request(self, conn):
        """访问目录"""
        view_path = input("请输入访问目录或文件夹的绝对路径:").strip()
        protocol["account"] = RoleBase.account_id
        protocol["password"] = RoleBase.account_pwd
        protocol["cmd"] = "view"
        protocol["data"] = view_path
        self.tell_server_length(protocol, conn)

    def view_files_response(self, data, conn, args):
        """访问目录服务器应答数据处理"""
        if data is not None:
            if data.startswith("no_permission"):
                print("\33[33;1m没有权限访问!\33[0m")
            elif data.startswith("path_error"):
                print("\33[33;1m路径错误!\33[0m")
            else:
                path, file_list = data.strip().split("*")
                self.set_cur_view_path(path)
                self.set_dir_files(" ".join(file_list.split("&")))
                print(path)
                print(" ".join(file_list.split("&")))
        else:
            print("服务器没有响应!")

    def upload_file_request(self, conn):
        """单任务上传请求"""
        upload_file_path = input("请输入要上传文件的绝对路径:").strip()
        if os.path.exists(upload_file_path):
            if os.path.isfile(upload_file_path):
                upload_file_path = upload_file_path
                upload_file_size = os.path.getsize(upload_file_path)
                file_name = ""
                remote_file_save_path = input("请输入服务器存储上传文件的目录路径:").strip()
                if remote_file_save_path.startswith(RoleBase.home_dir):
                    protocol["account"] = RoleBase.account_id
                    protocol["password"] = RoleBase.account_pwd
                    protocol["cmd"] = "upload"
                    protocol["data"] = remote_file_save_path + "*" + file_name + "*" + str(upload_file_size)
                    self.tell_server_length(protocol, conn)
                    return upload_file_path, upload_file_size
                else:
                    print("服务器存储路径错误")
            else:
                print("不是一个文件")
        else:
            print("上传文件的路径不存在")

    def upload_file_response(self, data, conn, args):
        """单任务上传请求服务器应答数据处理"""
        if data.startswith("READY"):
            """可以开始上传文件了"""
            self.thread_upload_file(None, conn, args)
        else:
            print("暂时无法上传文件")

    def download_file_request(self, conn):
        """单任务下载请求"""
        download_file_name = ""
        download_remote_file_path = input("请输入要下载文件的绝对路径:").strip()
        local_download_save_path = input("请输入要保存下载文件的本地路径").strip()
        if os.path.isdir(local_download_save_path):
            if download_remote_file_path.startswith(RoleBase.home_dir):  # 路径是否正确
                download_file_name = ""  # 缺解析
                protocol["account"] = RoleBase.account_id
                protocol["password"] = RoleBase.account_pwd
                protocol["cmd"] = "download"
                protocol["data"] = download_remote_file_path
                self.tell_server_length(protocol, conn)
                return local_download_save_path + download_file_name
            else:
                print("输入下载路径有误")
        else:
            print("输入本地存储路径有误")

    def download_file_response(self, data, conn, args):
        """
        单任务下载请求服务器应答数据处理
        :param data: 下载文件的总大小 or "file_not_exists"
        :param conn:
        :param args: 下载文件本地存储路径
        :return:
        """
        if data == "file_not_exists":
            return False
        else:
            """可以下载文件了,将下载文件的信息写入主程序的目录下的db/download_reocrd/xxx文件里面"""
            """格式是字符串：本地存储路径*文件总大小*已下载文件大小"""
            record_path = settings.source_dist.get("download_record_path") + os.sep + settings.DOWNLOAD_RC_FILE_NAME
            # if os.path.exists(record_path):
            with open(record_path, "a") as f:
                f.writelines(args*data*"0" + "\n")
            # else:
            #     pass
            self.thread_down_file(None, conn, args)
            return True

    def deal_server_response_datas(self, conn, args):
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
                    self.process_server_response(response_protocol, conn, args)

    def thread_upload_file(self, data, conn, args):
        """
        单个文件上传处理
        :param args: 上传文件的本次存储路径, 总大小
        :param data: 结果("SUCCESS")or"(FAILE)*累积收到的文件大小
        :return:
        """
        offset = 0
        server_file_length = 0
        upload_file_path = ""
        upload_file_path = args[0]
        total_file_size = int(args[1])
        if not data:
            pass
        else:
            result, server_file_length = data.strip().split("*")
            print("累计上传的文件大小:", int(server_file_length))
            if result == "SUCCESS":
                self.upload_file_offset = offset
                print("上传文件的总大小:", total_file_size)
                if int(server_file_length) == total_file_size:
                    print("\033[33;1m上传完成\033[0m")
                    return 1

        offset = int(server_file_length)
        uf = open(upload_file_path, "rb")
        if uf.readable():
            response_protocol = {}
            uf.seek(offset, 0)
            protocol["account"] = RoleBase.account_id
            protocol["password"] = RoleBase.account_pwd
            protocol["cmd"] = "uploading"
            protocol["data"] = uf.read(2 * 1024)  # 一次读2K
            self.tell_server_length(protocol, conn)
        uf.close()

    def thread_down_file(self, data, conn, args):
        """

        :param data: None：表示第一次创建文件。否则：表示已经接收到服务器发来的下载文件数据
        :param conn:
        :param args: 本地存储下载文件的路径
        :return:
        """
        local_path = ""
        local_path = str(args[0]).strip()
        protocol["account"] = RoleBase.account_id
        protocol["password"] = RoleBase.account_pwd
        protocol["cmd"] = "downloading"
        if not data: # 创建本地存储文件
            if os.path.exists(local_path):
                with open(local_path, "wb") as f:
                    pass
            else:
                os.mknod(local_path)
            protocol["data"] = "SUCCESS" + "0"
        else:
            record_path = settings.source_dist.get("download_record_path") + os.sep + settings.DOWNLOAD_RC_FILE_NAME
            cur_size = 0
            total_size = 0
            with open(record_path, "r") as f:
                while True:
                    reocrd_datas = f.readline()
                    if not reocrd_datas:
                        break
                    else:
                        path, total_size, cur_size = reocrd_datas.strip().split("*")
                        if local_path == path:
                            had_got_size = cur_size
                            break

            if data.startswith("SUCCESS"):
                result, recv_data = data.strip().split("*")
                now_size = cur_size + len(recv_data)
                if now_size < total_size:
                    with open(local_path, "ab") as f:  # 写本地存储文件
                        f.write(recv_data)
                    with open(record_path, "r") as rf, \
                        open(record_path + '.tmp', "w") as wf:  # 修改下载记录文件
                        while True:
                            reocrd_datas = rf.readline()
                            if not reocrd_datas:
                                break
                            else:
                                path, total_size, cur_size = reocrd_datas.strip().split("*")
                                if local_path == path:
                                    wf.writelines(args*total_size*str(now_size) + "\n")
                                else:
                                    wf.writelines(reocrd_datas + "\n")
                        os.remove(record_path)
                        os.rename(record_path + '.tmp', record_path)
                    protocol["data"] = "SUCCESS" + str(now_size)
                else:
                    print("下载完成了!")
            else:
                protocol["data"] = "FAILE" + "0"
                print("下载失败")
                # 这里后面将下载未完成用于断点续传的信息保存下来

        self.tell_server_length(protocol, conn)

    def upload_multi_files(self):
        """多任务上传"""
        pass

    def download_multi_files(self):
        """多任务下载"""
        pass

    def resume_tasks(self):
        """断点续传"""
        pass

    func_dict = {"login": login_result, "view": view_files_response, "upload": upload_file_response,
                 "uploading": thread_upload_file, "download": download_file_response, "downloading": thread_down_file}
