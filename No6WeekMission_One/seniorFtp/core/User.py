import os
import threading
import math
import queue
from core import RoleBase
from conf import settings
protocol = {"account": "", "password": "", "cmd": "", "data": ""}
_MAX_THREAD_NUMBER = 4
_MAX_UPLOAD_THREAD_NUMBER = 2

class Section(object):
    offset = 0
    size = 0

    def __init__(self, offset, size):
        self.offset = offset
        self.size = size


def init_queue(file_size):
    q = queue.Queue()
    average_size = int(file_size/_MAX_THREAD_NUMBER)
    for i in range(0, _MAX_THREAD_NUMBER):
        offset = average_size*i
        if i == _MAX_THREAD_NUMBER - 1:
            if (file_size % _MAX_THREAD_NUMBER) != 0:
                average_size += file_size % _MAX_THREAD_NUMBER
        s = Section(offset, average_size)
        q.put(s)

    return q


class User(RoleBase):
    """普通用户类"""
    is_login = False

    def __init__(self, client):
        super(User, self).__init__(client)
        self.client = client
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

    def view_files_request(self):
        """访问目录"""
        view_path = input("请输入访问目录或文件夹的绝对路径:").strip()
        protocol["account"] = RoleBase.account_id
        protocol["password"] = RoleBase.account_pwd
        protocol["cmd"] = "view"
        protocol["data"] = view_path
        conn = self.client.new_socket()
        self.request_server(protocol, conn)  # 向服务器请求数据
        tuple_params = ()
        self.deal_server_response_datas(conn, tuple_params)  # 接收服务器的应答

    def view_files_response(self, data):
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

    def download_file_request(self):
        """单任务下载请求"""
        download_remote_file_path = input("请输入要下载文件的绝对路径:").strip()
        local_download_save_dir = input("请输入要保存下载文件的本地路径").strip()
        if os.path.isdir(local_download_save_dir):
            if download_remote_file_path.startswith(RoleBase.home_dir):  # 路径是否正确
                conn = self.client.new_socket()
                download_file_name = ""  # 缺解析
                protocol["account"] = RoleBase.account_id
                protocol["password"] = RoleBase.account_pwd
                protocol["cmd"] = "download"
                protocol["data"] = download_remote_file_path
                self.request_server(protocol, conn)  # 发送请求给服务器
                # return local_download_save_path + download_file_name
                local_download_save_path = local_download_save_dir + download_file_name
                self.deal_server_response_datas(conn, local_download_save_path)  # 接收服务器的应答
            else:
                print("输入下载路径有误")
        else:
            print("输入本地存储路径有误")

    def download_file_response(self, data, conn, args):
        """
        单任务下载请求服务器应答数据处理
        :param data: 下载文件的总大小 or "file_not_exists"
        :param conn: socket
        :param args: 下载文件 de 本地存储路径
        :return:
        """
        if data == "file_not_exists":
            conn.close()
        else:
            """可以下载文件了,将下载文件的信息写入主程序的目录下的db/download_reocrd/xxx文件里面"""
            """格式是字符串：本地存储路径*文件总大小*已下载文件大小"""
            # record_path = settings.source_dist.get("download_record_path") + os.sep + settings.DOWNLOAD_RC_FILE_NAME
            # with open(record_path, "a") as f:
            #     f.writelines(args*data*"0" + "\n")
            self.create_download_file_missions(data, conn, args)

    def upload_file_request(self):
        """单任务上传请求"""
        upload_file_path = input("请输入要上传文件的绝对路径:").strip()
        if os.path.exists(upload_file_path):
            if os.path.isfile(upload_file_path):
                upload_file_path = upload_file_path
                upload_file_size = os.path.getsize(upload_file_path)
                file_name = ""
                remote_file_save_path = input("请输入服务器存储上传文件的目录路径:").strip()
                if remote_file_save_path.startswith(RoleBase.home_dir):
                    conn = self.client.new_socket()
                    protocol["account"] = RoleBase.account_id
                    protocol["password"] = RoleBase.account_pwd
                    protocol["cmd"] = "upload"
                    protocol["data"] = remote_file_save_path + "*" + file_name + "*" + str(upload_file_size)
                    self.tell_server_length(protocol, conn)
                    tuple_params = (upload_file_path, )
                    self.request_server(protocol, conn)  # 发送请求给服务器
                    self.deal_server_response_datas(conn, tuple_params)  # 接收服务器的应答
                else:
                    print("服务器存储路径错误")
            else:
                print("不是一个文件")
        else:
            print("上传文件的路径不存在")

    def upload_file_response(self, data, conn, args):
        """单任务上传请求服务器应答数据处理
        :param args: 上传文件的本地存储路径
        """
        if data.startswith("READY"):
            """可以开始上传文件了"""
            self.create_upload_file_missions(conn, args)
        else:
            print("暂时无法上传文件")
            conn.close()

    def deal_server_response_datas(self, conn, args):
        """服务器对客户端请求的应答"""
        running_flag = True
        while running_flag:
            server_final_ack = conn.get_response()
            if not server_final_ack:
                continue
            total_rece_size = int(server_final_ack)  # 要接收的应答数据的大小
            self.send_request(total_rece_size)  # 返回告知服务器知道即将接收的数据大小了
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
                    running_flag = False

    @staticmethod
    def process_server_response(data, conn, args):
        """处理流程自动选择进行"""
        if isinstance(data, dict):
            cmd = data.get("cmd")
            if cmd is not None:
                User.func_dict[cmd](data.get("data"), conn, args)

    def create_upload_file_missions(self, conn, args):
        """
        创建多线程用于上传文件, 生产者
        :param conn: socket
        :param args: 待上传文件的路径
        :return:
        """
        if os.path.exists(args):
            if os.path.isfile(args):
                q = init_queue(os.path.getsize(args))
                for i in range(0, _MAX_THREAD_NUMBER):
                    t = threading.Thread(target=self.upload_thread_body, args=(self.client.new_socket(), args, q, ))
                    t.setDaemon(True)
                    t.start()
                q.join()
            else:
                conn.close()
                print("不是个文件")
        else:
            conn.close()
            print("路径不存在")

    def create_download_file_missions(self, data, conn, args):
        """
        创建多线程用于下载文件, 生产者
        :param data: 下载文件的总大小
        :param conn: socket
        :param args: 本地存储下载文件的路径
        :return:
        """

        protocol["account"] = RoleBase.account_id
        protocol["password"] = RoleBase.account_pwd
        protocol["cmd"] = "downloading"
        if data.isdigit():  # 全数字 创建本地存储文件
            local_path = ""
            local_path = str(args[0]).strip()
            if os.path.exists(local_path):
                os.remove(local_path)
            else:
                os.mknod(local_path)
            protocol["data"] = "SUCCESS" + "0"
            self.request_server(protocol, conn)
        else:
            conn.close()
            return
        # 创建多线程下载
        q = init_queue(data)
        for i in range(0, _MAX_THREAD_NUMBER):
            t = threading.Thread(target=self.download_thread_body, args=(self.client.new_socket(), local_path, q, ))
            t.setDaemon(True)
            t.start()
        q.join()

    def upload_thread_body(self, conn, save_path, q):
        """
        消费者
        :param conn: socket
        :param save_path: 上传文件 本地 存储路径
        :param q: Section的实例
        :return:
        """
        while not q.empty():
            section = q.get()
            offset = section.offset
            size = section.size
            tuple_param = (save_path, offset, size, )
            self.thread_upload_file(None, conn, tuple_param)
            q.task_done()

    def download_thread_body(self, conn, save_path, q):
        """
        消费者
        :param conn: socket
        :param save_path: 下载文件 本地 存储路径
        :param q :  Section的实例
        :return:
        """
        while not q.empty():
            section = q.get()
            offset = section.offset
            size = section.size
            tuple_params = (save_path, offset, size, 0, )
            self.deal_server_response_datas(conn, tuple_params)
            q.task_done()

    def thread_upload_file(self, data, conn, args):
        """
        文件上传
        :param args: 上传文件的 本地 存储路径, 读取起始地址, 每次读取大小
        :param data: None(第一次读) 或者 结果("SUCCESS")or"(FAILE)*收到的文件大小
        :return:
        """
        file_save_path = str(args[0])
        offset = int(args[1])
        size = int(args[2])
        if not data:
            protocol["account"] = RoleBase.account_id
            protocol["password"] = RoleBase.account_pwd
            protocol["cmd"] = "uploading"
            uf = open(file_save_path, "rb")
            if uf.readable():
                uf.seek(offset, 0)
                protocol["account"] = RoleBase.account_id
                protocol["password"] = RoleBase.account_pwd
                protocol["cmd"] = "uploading"
                if size > 2 * 1024:
                    protocol["data"] = uf.read(2 * 1024)  # 一次读2K
                else:
                    protocol["data"] = uf.read(size)  # 一次读 size
                tuple_params = (file_save_path, offset, size, )
                self.request_server(protocol, conn)
                self.deal_server_response_datas(conn, tuple_params)
            uf.close()
        else:
            if data.startswith("SUCCESS"):
                result, server_get_length = data.strip().split("*")
                print("累计上传的文件大小:", int(server_get_length))
                if result == "SUCCESS":
                    if int(server_get_length) == os.path.getsize(file_save_path):
                        print("\033[33;1m上传完成\033[0m")
                    else:
                        uf = open(file_save_path, "rb")
                        if uf.readable():
                            response_protocol = {}
                            uf.seek(offset, 0)
                            protocol["account"] = RoleBase.account_id
                            protocol["password"] = RoleBase.account_pwd
                            protocol["cmd"] = "uploading"
                            if size > 2 * 1024:
                                protocol["data"] = uf.read(2 * 1024)  # 一次读2K
                            else:
                                protocol["data"] = uf.read(size)  # 一次读 size

                            tuple_params = (file_save_path, offset + server_get_length, size - server_get_length)
                            self.deal_server_response_datas(conn, tuple_params)
                        uf.close()
                elif result == "FAILE":
                    print("上传失败")
                    conn.close()
            else:
                conn.close()
                print("***调用记录方法***记录到上传文件信息记录文件,用于断点续传")

    def thread_down_file(self, data, conn, args):
        """
        本地下载写文件
        :param data: 表示已经接收到服务器发来的下载文件数据"SUCCESS" or "FAILE*文件数据
        :param conn: socket
        :param args: 本地存储下载文件的路径, 下载起始偏移量, 下载大小, 已接收到文件数据长度
        :return:
        """

        protocol["account"] = RoleBase.account_id
        protocol["password"] = RoleBase.account_pwd
        protocol["cmd"] = "downloading"
        local_path = args[0]
        offset = int(args[1])
        size = int(args[2])
        had_got_size = int(args[3])
        if data.startswith("SUCCESS"):
            result, recv_data = data.strip().split("*")
            now_size = had_got_size + len(recv_data)
            if now_size < size:
                with open(local_path, "ab") as f:  # 写本地存储文件
                    f.seek(offset, 0)
                    f.write(recv_data)
                protocol["data"] = "SUCCESS" + str(now_size)
                self.request_server(protocol, conn)
                tuple_params = (local_path, offset, size, now_size, )
                self.deal_server_response_datas(conn, tuple_params)
            else:
                print("下载完成了!")
                conn.close()
        else:
            protocol["data"] = "FAILE" + "0"
            print("下载失败")
            conn.close()
            # 将下载未完成用于断点续传的信息保存下来


        # record_path = settings.source_dist.get("download_record_path") + os.sep + settings.DOWNLOAD_RC_FILE_NAME
        # had_got_size = 0
        # total_size = 0
        # with open(record_path, "r") as f:
        #     while True:
        #         reocrd_datas = f.readline()
        #         if not reocrd_datas:
        #             break
        #         else:
        #             path, total_size, cur_size = reocrd_datas.strip().split("*")
        #             local_path = str(args[0]).strip()
        #             if local_path == path:
        #                 had_got_size = cur_size  # 下载记录文件里面当前下载文件已经下载的大小
        #                 break

    def write_download_record(self, record_path, args, now_size):
        """写下载记录文件
        :param record_path: 本地下载记录的路径
        :param args: 本地下载文件的路径
        :now_size: 已经下载的文件大小
        """
        local_path = str(args[0]).strip()  # 获得当前下载文件本地存储路径
        with open(record_path, "r") as rf, \
                open(record_path + '.tmp', "w") as wf:  # 修改下载记录文件
            while True:
                reocrd_datas = rf.readline()
                if not reocrd_datas:
                    break
                else:
                    path, total_size, cur_size = reocrd_datas.strip().split("*")
                    if local_path == path:  # 在下载记录文件中找  是否 存在这个文件路径, 存在就更新对应下载文件在下载记录里面的信息
                        wf.writelines(args * total_size * str(now_size) + "\n")
                    else:
                        wf.writelines(reocrd_datas + "\n")
            os.remove(record_path)
            os.rename(record_path + '.tmp', record_path)

    def write_upload_record(self):
        """写上传记录文件"""
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

    func_dict = {"login": login_result, "view": view_files_response, "upload": upload_file_response,
                 "uploading": thread_upload_file, "download": download_file_response, "downloading": thread_down_file}
