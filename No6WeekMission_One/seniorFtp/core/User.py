import os
import threading
import math
import queue
import shelve
from core import RoleBase
from conf import settings
from core import FtpClient

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
    file_size = int(file_size)
    q = queue.Queue()
    average_size = int(file_size/_MAX_THREAD_NUMBER)
    for i in range(0, _MAX_THREAD_NUMBER):
        offset = average_size*i
        if i == _MAX_THREAD_NUMBER - 1:
            if (file_size % _MAX_THREAD_NUMBER) != 0:
                average_size += file_size % _MAX_THREAD_NUMBER
        print("第 %d 段偏移量起始: %d" % (i, offset))
        print("区间下载大小: %d" % average_size)
        s = Section(offset, average_size)
        q.put(s)

    return q


class User(RoleBase.RoleBase):
    """普通用户类"""
    is_login = False

    def __init__(self, client, name, pwd):
        super(User, self).__init__(client, name, pwd)
        self.client = client
        self.view_path = ""
        self.dir_files = ""
        self.upload_file_path = ""  # 待上传文件的绝对路径
        self.upload_file_size = 0  # 上传文件的总大小
        self.upload_file_offset = 0  # 已上传文件的大小
        self.download_file_path = ""
        self.upload_files_list = {}  # 待上传个文件的绝对路径字典
        self.download_files_list = []

    def login_result(self, data, client, args):
        home_dir = ""
        files_list = ""
        if isinstance(data, int):
            is_login_statue = int(data)
        else:
            is_login_statue, home_dir, files_list = data.strip().split("*")
            is_login_statue = int(is_login_statue)
        if is_login_statue == 1:
            print("\033[32;1m登陆成功\033[0m")
            self.update_login_statue(True)
            self.set_default_home_path(home_dir)
            self.set_cur_view_path(home_dir)
            self.set_dir_files(",".join(files_list.split("&")))
        elif is_login_statue == 0:
            print("\033[35;1m账户不存在!\033[0m")
            self.update_login_statue(False)
        elif is_login_statue == 9:
            print("\033[35;1m账户异常,无法登录,请联系管理员!\033[0m")
            self.update_login_statue(False)
        elif is_login_statue == 2:
            print("\033[35;1m用户名或密码错误!\033[0m")

    def show_cur_files(self):
        print(self.get_cur_view_path())
        print(self.get_dir_files())

    def view_files_request(self):
        """访问目录"""
        view_path = input("请输入访问目录或文件夹的绝对路径:").strip()
        protocol["account"] = RoleBase.RoleBase.account_id
        protocol["password"] = RoleBase.RoleBase.account_pwd
        protocol["cmd"] = "view"
        protocol["data"] = view_path
        self.request_server(protocol, self.client)  # 向服务器请求数据

    def view_files_response(self, data, client, args):
        """访问目录服务器应答数据处理"""
        if data is not None:
            if data.startswith("没有访问权限"):
                print("\33[33;1m没有权限访问!\33[0m")
            elif data.startswith("路径不存在"):
                print("\33[33;1m路径错误!\33[0m")
            else:
                path, file_list = data.strip().split("*")
                self.set_cur_view_path(path)
                self.set_dir_files(" ".join(file_list.split("&")))
                # print(path)
                # print(" ".join(file_list.split("&")))
        else:
            print("服务器没有响应!")

    def download_file_request(self):
        """单任务下载请求"""
        download_remote_file_path = input("请输入要下载文件的远程路径:").strip()
        local_download_save_dir = input("请输入要保存下载文件的本地路径").strip()
        if os.path.isdir(local_download_save_dir):
            if download_remote_file_path.startswith(self.get_default_home_path()):  # 路径是否正确
                download_file_name = os.path.split(download_remote_file_path)[1].strip()
                print("下载文件名是: ", download_file_name)
                protocol["account"] = RoleBase.RoleBase.account_id
                protocol["password"] = RoleBase.RoleBase.account_pwd
                protocol["cmd"] = "download"
                protocol["data"] = download_remote_file_path
                self.request_server(protocol, self.client)  # 发送请求给服务器
                local_download_save_path = local_download_save_dir + "\\" + download_file_name
                tuple_params = (download_remote_file_path, local_download_save_path,)
                self.deal_server_response_datas(self.client, tuple_params)  # 接收服务器的应答
            else:
                print("输入下载路径有误")
        else:
            print("输入本地存储路径有误")

    def download_file_response(self, data, client, args):
        """
        单任务下载请求服务器应答数据处理
        :param data: 下载文件的总大小 or "file_not_exists"
        :param client: ftpclient
        :param args: 服务器文件存储路径, 下载文件 de 本地存储路径
        :return:
        """
        if data == "file_not_exists":
            client.close_socket()
        else:
            """可以下载文件了,将下载文件的信息写入主程序的目录下的db/download_reocrd/xxx文件里面"""
            """格式是字符串：本地存储路径*文件总大小*已下载文件大小"""
            # record_path = settings.source_dist.get("download_record_path") + os.sep + settings.DOWNLOAD_RC_FILE_NAME
            # with open(record_path, "a") as f:
            #     f.writelines(args*data*"0" + "\n")
            self.create_download_file_missions(data, client, args)

    def upload_file_request(self):
        """单任务上传请求"""
        upload_file_path = input("请输入要上传文件的绝对路径:").strip()
        if os.path.exists(upload_file_path):
            if os.path.isfile(upload_file_path):
                upload_file_path = upload_file_path
                upload_file_size = os.path.getsize(upload_file_path)
                file_name = ""
                remote_file_save_dir = input("请输入服务器存储上传文件的目录路径:").strip()
                if remote_file_save_dir.startswith(RoleBase.home_dir):
                    conn = self.client.new_socket()
                    protocol["account"] = RoleBase.RoleBase.account_id
                    protocol["password"] = RoleBase.RoleBase.account_pwd
                    protocol["cmd"] = "upload"
                    protocol["data"] = remote_file_save_dir + "*" + file_name + "*" + str(upload_file_size)
                    self.tell_server_length(protocol, conn)
                    tuple_params = (upload_file_path, remote_file_save_dir, )
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
        :param args: 上传文件的本地存储路径, 服务器上文件存储目录路径
        """
        if data.get("data").startswith("READY"):
            """可以开始上传文件了"""
            self.create_upload_file_missions(conn, args)
        else:
            print(data.get("data"))
            conn.close()

    def deal_server_response_datas(self, client, args):
        """服务器对客户端请求的应答"""
        running_flag = True
        while running_flag:
            server_final_ack = client.get_response()
            if not server_final_ack:
                continue
            total_rece_size = int(server_final_ack)  # 要接收的应答数据的大小
            print("接收服务器应答数据长度", total_rece_size)
            client.send_request(total_rece_size)  # 返回告知服务器知道即将接收的数据大小了
            received_size = 0
            res_data = b''

            while received_size != total_rece_size:
                cmd_res = client.get_response()
                if not cmd_res:
                    continue
                received_size += len(cmd_res.decode())
                res_data += cmd_res
                if received_size == total_rece_size:
                    print("接收数据完成")
                    response_protocol = eval(str(res_data.decode()))
                    print("server response:", response_protocol)
                    self.process_server_response(response_protocol, client, args)
                    running_flag = False
                    break

    def process_server_response(self, data, client, args):
        """处理流程自动选择进行"""
        if isinstance(data, dict):
            cmd = data.get("cmd")
            if cmd is not None:
                User.func_dict.get(cmd)(self, data.get("data"), client, args)

    def create_upload_file_missions(self, conn, args):
        """
        创建多线程用于上传文件, 生产者
        :param conn: socket
        :param args: 待上传文件的本地路径 要上传到服务器上的目录路径
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

    def create_download_file_missions(self, data, client, args):
        """
        创建多线程用于下载文件, 生产者
        :param data: 下载文件的总大小
        :param client: ftpclient
        :param args: 服务器存储文件路径, 本地存储下载文件的路径
        :return:
        """
        # 创建多线程下载
        q = init_queue(data)
        for i in range(0, _MAX_THREAD_NUMBER):
            new_client = FtpClient.FtpClient(client.host, client.port)
            new_client.new_socket()
            t = threading.Thread(target=self.download_thread_body, args=(new_client, args, q, ))
            t.setDaemon(True)
            t.start()
        q.join()

    def upload_thread_body(self, conn, args, q):
        """
        消费者
        :param conn: socket
        :param args: 上传文件 本地 存储路径,  要上传到服务器上的目录路径
        :param q: Section的实例
        :return:
        """
        while not q.empty():
            section = q.get()
            offset = section.offset
            size = section.size
            tuple_param = (args[0], args[1], offset, size, )
            self.thread_upload_file(None, conn, tuple_param)
            q.task_done()

    def download_thread_body(self, client, args, q):
        """
        消费者
        :param client: client
        :param args: 服务器文件存储路径, 下载文件 本地 存储路径
        :param q :  Section的实例
        :return:
        """
        while not q.empty():
            section = q.get()
            offset = section.offset
            size = section.size
            tuple_params = (str(args[0]), str(args[1]), offset, size,)
            self.thread_down_file(None, client, tuple_params)
            q.task_done()
        client.close_socket()

    def thread_upload_file(self, data, conn, args):
        """
        本地文件上传
        :param args: 上传文件的 本地 存储路径, 要上传到服务器上的路径, 读取起始地址, 待上传大小
        :param data: None(第一次读) 或者 结果("SUCCESS")or"(FAILE)*收到的文件大小
        :return:
        """
        file_save_path = str(args[0])
        remote_save_path = str(args[1])
        offset = int(args[2])
        size = int(args[3])
        if not data:
            protocol["account"] = RoleBase.RoleBase.account_id
            protocol["password"] = RoleBase.RoleBase.account_pwd
            protocol["cmd"] = "uploading"
            uf = open(file_save_path, "rb")
            if uf.readable():
                uf.seek(offset, 0)
                if size > 2 * 1024:
                    data = uf.read(2 * 1024)  # 一次读2K
                else:
                    data = uf.read(size)  # 一次读 size
                protocol["data"] = remote_save_path + "*" + os.path.split(file_save_path)[1] + "*" + str(offset) + "*" + str(len(data)) + "*" + data  # 数据放最后 免得每次+重新分配内存导致的效率低
                self.request_server(protocol, conn)
                tuple_params = (file_save_path, offset, size,)
                self.deal_server_response_datas(conn, tuple_params)
            uf.close()
        else:
            if data.startswith("SUCCESS"):
                result, server_get_length = data.strip().split("*")
                print("累计上传的文件大小:", int(server_get_length))
                if result == "SUCCESS":
                    if int(server_get_length) == size:
                        print("\033[33;1m上传完成\033[0m")
                    else:
                        uf = open(file_save_path, "rb")
                        if uf.readable():
                            uf.seek(offset, 0)
                            protocol["account"] = RoleBase.account_id
                            protocol["password"] = RoleBase.account_pwd
                            protocol["cmd"] = "uploading"
                            if size > 2 * 1024:
                                data = uf.read(2 * 1024)  # 一次读2K
                            else:
                                data = uf.read(size)  # 一次读 size
                            protocol["data"] = str(offset) + "*" + str(len(data)) + str(data)
                            self.request_server(protocol, conn)
                            tuple_params = (file_save_path, offset + server_get_length, size - server_get_length)
                            self.deal_server_response_datas(conn, tuple_params)
                        uf.close()
                elif result == "FAILE":
                    print("上传失败")
                    conn.close()
            else:
                conn.close()
                print("***调用记录方法***记录到上传文件信息记录文件,用于断点续传")

    def thread_down_file(self, data, client, args):
        """
        远程服务器文件本地下载写
        :param data: 表示已经接收到服务器发来的下载文件数据"SUCCESS" or "FAILE*文件数据
        :param client: client
        :param args: 服务器文件路径, 本地存储下载文件的路径, 下载起始偏移量, 待下载文件大小
        :return:
        """
        file_remote_save_path = args[0]
        local_path = args[1]
        offset = args[2]
        remain_size = args[3]  # 剩余下载大小
        print("剩余下载大小:------------------ ", remain_size)
        protocol["account"] = RoleBase.RoleBase.account_id
        protocol["password"] = RoleBase.RoleBase.account_pwd
        protocol["cmd"] = "downloading"
        if not data:
            # "SUCCESS" * 请求读取文件起始位置 * 请求大小 or "FAILE*0
            if os.path.exists(local_path):
                os.remove(local_path)
            with open(local_path, "wb") as f:
                pass

            request_size = 0
            if remain_size > 2 * 1024:
                request_size = 2 * 1024
            else:
                request_size = remain_size
            print("下载路径:", file_remote_save_path)
            print("偏移量:", offset)
            print("请求下载大小", request_size)
            protocol["data"] = file_remote_save_path + "*" + str(offset) + "*" + str(request_size)
            self.request_server(protocol, client)
            tuple_params = (file_remote_save_path, local_path, offset, remain_size,)
            self.deal_server_response_datas(client, tuple_params)
        else:
            if data != "FAILE":
                recv_data = b''
                recv_data = data
                recv_data_size = len(recv_data)
                if remain_size >= recv_data_size:
                    remain_size -= recv_data_size
                print("下载路径:", file_remote_save_path)
                print("偏移量:", offset)
                print("接收到的数据大小:---------------", recv_data_size)
                if remain_size == 0:
                    print("下载完成了!")
                    client.close_socket()
                else:
                    with open(local_path, "ab") as f:  # 写本地存储文件,这里有有个坑，最好以管理员身份运行，要不然可能会报错：提示没有权限写
                        f.seek(offset, 0)
                        f.write(recv_data.encode())
                    request_size = 0
                    if remain_size > 2 * 1024:
                        request_size = 2 * 1024
                    else:
                        request_size = remain_size
                    print("请求下载大小", request_size)
                    protocol["data"] = file_remote_save_path + "*" + str(offset) + "*" + str(request_size)
                    self.request_server(protocol, client)
                    tuple_params = (file_remote_save_path, local_path, offset + recv_data_size, remain_size,)
                    self.deal_server_response_datas(client, tuple_params)
            else:
                protocol["data"] = "FAILE" + "0"
                print("下载失败")
                client.close_socket()
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
