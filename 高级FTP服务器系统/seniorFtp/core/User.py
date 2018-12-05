import os
import stat
import threading
import math
import queue
import shelve
import time
import signal
import json
from core import RoleBase
from conf import settings
from core import FtpClient
from core import common_func

protocol = {"account": "", "password": "", "cmd": "", "data": ""}
protocol_up = {"account": "", "password": "", "cmd": "", "data": {"head": "", "content": ""}}
_MAX_THREAD_NUMBER = 4   # 由于GIL的关系，多线程的做法实在不好掌控放弃
_MAX_UPLOAD_THREAD_NUMBER = 2

msg_queue = queue.Queue()
download_task_queue = queue.Queue()

request_send_queue = queue.Queue()  # 请求服务器发送时消息队列
# print(request_send_queue)

# L = threading.Lock()
# print("创建锁:", L)


def init_queue():
    q = queue.Queue()
    return q


def add_queue_task(task_queue, file_size, start_pos, section_number=_MAX_THREAD_NUMBER):
    file_size = int(file_size)
    average_size = int(file_size / section_number)
    for i in range(0, section_number):
        offset = average_size * i + start_pos
        if i == section_number - 1:
            if (file_size % section_number) != 0:
                average_size += file_size % section_number
        # print("第 %d 段偏移量起始: %d" % (i, offset))
        # print("区间下载大小: %d" % average_size)
        s = Section(offset, average_size)
        task_queue.put(s)


class RequestTask(object):

    def __init__(self, client, data):
        self.client = client
        self.data = data


class Section(object):
    offset = 0
    size = 0

    def __init__(self, offset, size):
        self.offset = offset
        self.size = size


class User(RoleBase.RoleBase):
    """普通用户类"""
    is_login = False
    upload_protocol = ("local_path", "offset", "remote_path")

    def __init__(self, client, name, pwd):
        super(User, self).__init__(client, name, pwd)
        self.client = client
        self.view_path = ""
        self.dir_files = ""
        self.upload_file_path = ""  # 待上传文件的绝对路径
        self.upload_file_size = 0  # 上传文件的总大小
        self.download_file_size = 0  # 下载文件的总大小
        self.upload_file_offset = 0  # 已上传文件的大小
        self.download_file_path = ""
        self.upload_files_list = {}  # 待上传个文件的绝对路径字典
        self.download_files_list = []
        self.upload_section = 1
        self.download_section = 1
        self.upload_section_size = 0
        self.upload_offset = 0  # 初始上传文件操作偏移量
        self.download_offset = 0  # 初始下载文件操作偏移量
        self.download_section_size = 0
        # self.pause_event = threading.Event()  # 上传下载中暂停事件 暂时做不了
        # self.quit_event = threading.Event()  # 上传下载中停止事件
        # self.download_over_flag = False
        # self.download_ing_flag = False

    # def event_control(self):
    #     while not self.quit_event.isSet():
    #         print("取消请输入: q")
    #         if self.download_over_flag:
    #             chose = 'q'
    #         else:
    #             chose = input().strip()
    #         print("您选择的是", chose)
    #         if chose == 'q':
    #             self.quit_event.set()
    #         time.sleep(0.2)
    # def shutdown_task(self, signum, frame):
    #     print("taks shutdown!")
    #     self.quit_event.set()
    #
    # def create_signal(self):
    #     try:
    #         signal.signal(signal.SIGINT, self.shutdown_task)
    #         signal.signal(signal.SIGTERM, self.shutdown_task)
    #         while True:
    #             time.sleep(0.5)
    #     except Exception as exc:
    #         print(exc)

    def login_result(self, data, client, args):
        home_dir = ""
        files_list = ""
        if isinstance(data, int):
            is_login_statue = int(data)
        else:
            is_login_statue, home_dir, files_list = data.strip().split("*")
            is_login_statue = int(is_login_statue)
        if is_login_statue == 1:
            print("\33[32;1m登陆成功\33[0m")
            self.update_login_statue(True)
            self.set_default_home_path(home_dir)
            self.set_cur_view_path(home_dir)
            self.set_dir_files(",".join(files_list.split("&")))
        elif is_login_statue == 0:
            print("\33[35;1m账户不存在!\33[0m")
            self.update_login_statue(False)
        elif is_login_statue == 9:
            print("\33[35;1m账户异常,无法登录,请联系管理员!\33[0m")
            self.update_login_statue(False)
        elif is_login_statue == 2:
            print("\33[35;1m用户名或密码错误!\33[0m")

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
        self.request_server(self.client, protocol)  # 向服务器请求数据

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
        local_download_save_dir = input("请输入要保存下载文件的本地路径:").strip()
        if os.path.isdir(local_download_save_dir):
            if download_remote_file_path.startswith(self.get_default_home_path()):  # 路径是否正确
                download_file_name = os.path.split(download_remote_file_path)[1].strip()
                local_download_save_path = local_download_save_dir + os.sep + download_file_name
                if os.path.exists(local_download_save_path):
                    print("文件已存在!")
                    return
                # print("下载文件名是: ", download_file_name)
                protocol["account"] = RoleBase.RoleBase.account_id
                protocol["password"] = RoleBase.RoleBase.account_pwd
                protocol["cmd"] = "download"
                protocol["data"] = download_remote_file_path
                self.request_server(self.client, protocol)  # 发送请求给服务器
                tuple_params = (download_remote_file_path, local_download_save_path,)
                self.deal_server_response_datas(self.client, tuple_params)  # 接收服务器的应答
            else:
                print("\33[33;1m输入下载路径有误\33[0m")
        else:
            print("\33[33;1m输入本地存储路径有误\33[0m")

    def download_file_response(self, data, client, args):
        """
        单任务下载请求服务器应答数据处理
        :param data: 下载文件的总大小 or "file_not_exists"
        :param client: ftpclient
        :param args: 服务器文件存储路径, 下载文件 de 本地存储路径
        :return:
        """
        if data == "文件不存在":
            print("文件不存在")
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
                file_name = os.path.basename(upload_file_path)
                remote_file_save_dir = input("请输入服务器存储上传文件的目录路径:").strip()
                if remote_file_save_dir.startswith(self.get_default_home_path()):
                    protocol["account"] = RoleBase.RoleBase.account_id
                    protocol["password"] = RoleBase.RoleBase.account_pwd
                    protocol["cmd"] = "upload"
                    protocol["data"] = remote_file_save_dir + "*" + file_name + "*" + str(upload_file_size)
                    self.request_server(self.client, protocol)  # 发送请求给服务器
                    tuple_params = (upload_file_path, remote_file_save_dir,)
                    self.deal_server_response_datas(self.client, tuple_params)  # 接收服务器的应答
                else:
                    print("服务器存储路径错误")
            else:
                print("不是一个文件")
        else:
            print("上传文件的路径不存在")

    def upload_file_response(self, data, client, args):
        """单任务上传请求服务器应答数据处理
        :param client: ftpclient
        :param args: 上传文件的本地存储路径, 服务器上文件存储目录路径
        """
        print(data)
        if data.startswith("READY"):
            """可以开始上传文件了"""
            has_upload_size = int(data.split("*")[1])
            self.create_upload_file_missions(client, args, has_upload_size)

    def deal_server_response_datas(self, client, args):
        """服务器对客户端请求的应答"""
        running_flag = True
        while running_flag:
            server_final_ack = client.get_response()
            if not server_final_ack:
                continue
            total_rece_size = int(server_final_ack)  # 要接收的应答数据的大小
            # print("接收服务器应答数据长度", total_rece_size)
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
                    # print("接收数据完成")
                    response_protocol = eval(str(res_data.decode()))
                    # print("server response:", response_protocol)
                    result = self.process_server_response(response_protocol, client, args)
                    if result is not None:
                        client = result[0]
                        args = result[1]
                    else:
                        running_flag = False
                    break

    def process_server_response(self, data, client, args):
        """处理流程自动选择进行"""
        if isinstance(data, dict):
            cmd = data.get("cmd")
            if cmd is not None:
                # print(data.get("data"))
                return User.func_dict.get(cmd)(self, data.get("data"), client, args)

    def create_upload_file_missions(self, client, args, has_upload_size):
        """
        创建多线程用于上传文件, 生产者
        :param client: ftpclient
        :param args: 待上传文件的本地路径 要上传到服务器上的目录路径
        :param has_upload_size: 服务器上这个文件已经上传的文件大小
        :return:
        """
        file_path = args[0]
        file_size = os.path.getsize(file_path) - has_upload_size
        if os.path.exists(file_path):
            if os.path.isfile(file_path):
                q = init_queue()
                add_queue_task(q, file_size, has_upload_size, 4)  # 分段个数可根据文件大小来调整
                # for i in range(0, _MAX_THREAD_NUMBER):
                # process_thread = threading.Thread(target=common_func.progress_bar, args=(self.section, 4,))
                # process_thread.setDaemon(True)
                # process_thread.start()
                self.upload_file_size = file_size
                new_client = FtpClient.FtpClient(client.host, client.port)
                new_client.new_socket()
                t = threading.Thread(target=self.upload_thread_body, args=(new_client, args, q, ))
                t.setDaemon(True)
                t.start()
                # q.join()
            else:
                print("不是个文件")
        else:
            print("路径不存在")

    def create_download_file_missions(self, data, client, args):
        """
        创建多线程用于下载文件, 生产者
        :param data: 下载文件的总大小
        :param client: ftpclient
        :param args: 服务器存储文件路径, 本地存储下载文件的路径
        :return:
        """
        # print("下载文件总大小：", int(data))
        # 创建多线程下载
        local_file_path = args[1]
        tmp_path = local_file_path + ".tmp"
        exists_size = 0
        if os.path.exists(tmp_path):
            exists_size = os.path.getsize(tmp_path)
        else:
            pass
        file_size = int(data) - exists_size
        q = init_queue()
        add_queue_task(q, file_size, exists_size, 4)  # 分段个数可根据文件大小来调整
        self.download_file_size = file_size
        # for i in range(0, _MAX_THREAD_NUMBER):
        new_client = FtpClient.FtpClient(client.host, client.port)
        new_client.new_socket()
        # self.create_signal()
        t = threading.Thread(target=self.download_thread_body, args=(new_client, args, q, ))
        t.setDaemon(True)
        t.start()

        # main_thread = threading.current_thread()
        # for t in threading.enumerate():
        #     if t is main_thread:
        #         continue
        #     t.join()
        # q.join()  # 是否阻塞调用主线程(根据实际情况调整吧)

    def upload_thread_body(self, client, args, q):
        """
        消费者
        :param client: client
        :param args: 上传文件 本地 存储路径,  要上传到服务器上的目录路径
        :param q: Section的实例
        :return:
        """
        while True:
            section = q.get()
            offset = section.offset
            size = section.size
            # print("初始offset = %d" % offset)
            # print("初始size = %d" % size)
            self.upload_offset = offset
            self.upload_section_size = size
            self.upload_section = round((offset / size) + 1)
            common_func.progress_bar(self.upload_section, 4, 0, size)
            tuple_param = (args[0], args[1], offset, size, )
            self.begin_upload_file_data(client, tuple_param)
            q.task_done()

    def download_thread_body(self, client, args, q):
        """
        消费者
        :param client: client
        :param args: 服务器文件存储路径, 下载文件 本地 存储路径
        :param q :  Section的实例
        :return:
        """
        # flow_control = threading.Thread(target=self.event_control)  # 下载流程控制
        # # flow_control.setDaemon(True)
        # flow_control.start()
        while not q.empty():
            # if self.quit_event.isSet():
            #      print("选择了停止")
            #      q.queue.clear()
            #      self.quit_event.clear()
            #     break
            # if self.pause_event.isSet():
            #     time.sleep(0.2)
            #     continue
            # else:
            section = q.get()
            offset = section.offset
            size = section.size
            # print("初始offset = %d" % offset)
            # print("初始size = %d" % size)
            self.download_section_size = size
            self.download_offset = offset
            self.download_section = round((offset / size) + 1)
            common_func.progress_bar(self.download_section, 4, 0, size)
            tuple_params = (str(args[0]), str(args[1]), offset, size, )
            self.begin_request_file_data(client, tuple_params)
            q.task_done()
            time.sleep(0.1)

    def begin_request_file_data(self, client, args):
        down_result = 0
        file_remote_save_path = args[0]
        local_path = args[1]
        tmp_local_path = local_path + ".tmp"
        offset = int(args[2])
        remain_size = int(args[3])  # 剩余下载大小
        protocol["account"] = RoleBase.RoleBase.account_id
        protocol["password"] = RoleBase.RoleBase.account_pwd
        protocol["cmd"] = "downloading"
        # "SUCCESS" * 请求读取文件起始位置 * 请求大小 or "FAILE*0

        if offset == 0:
            if os.path.exists(tmp_local_path) is False:
                # print(tmp_local_path)
                # print("第一次写文件需要判断原来是否已经存在文件,存在则删除原来的新建")
                # os.chmod(local_path, stat.S_IRWXG)
                with open(tmp_local_path, "wb") as f:
                    pass

        request_size = 0
        if remain_size > 10 * 1024:
            request_size = 10 * 1024
        else:
            request_size = remain_size
        # print("下载路径:", file_remote_save_path)
        # print("初始偏移量:", offset)
        # print("下载总大小:------------------", remain_size)
        # print("请求下载大小", request_size)
        protocol["data"] = file_remote_save_path + "*" + str(offset) + "*" + str(request_size)
        # s = RequestTask(client, protocol)
        # request_send_queue.put(s)
        self.write_download_record(local_path, offset, file_remote_save_path)
        self.request_server(client, protocol)
        # t = threading.Thread(target=self.request_server, args=(client, protocol, ))
        # t.start()
        # t.join()
        tuple_params = (file_remote_save_path, local_path, offset, remain_size,)
        self.deal_server_response_datas(client, tuple_params)

    def begin_upload_file_data(self, client, args):
        file_save_path = str(args[0])
        # print("要上传文件的名称:", file_save_path)
        remote_save_path = str(args[1])
        # print("远程存储路径:", remote_save_path)
        offset = int(args[2])
        size = int(args[3])
        # print("偏移量: %d 待传大小 %d" % (offset, size))
        protocol_up["account"] = RoleBase.RoleBase.account_id
        protocol_up["password"] = RoleBase.RoleBase.account_pwd
        protocol_up["cmd"] = "uploading"
        uf = open(file_save_path, "rb")
        if uf.readable():
            uf.seek(offset, 0)
            if size > 5 * 1024:
                file_data = uf.read(5 * 1024)  # 一次读2K
            else:
                file_data = uf.read(size)  # 一次读 size
            code_format = common_func.string_encoding(file_data)
            # print("文件编码格式: ", code_format)
            # print(file_data)
            # length = len(file_data)
            # file_data = file_data.decode("utf-8")  # 这个方法并不稳定,建议少用!
            # print(type(file_data))
            # print(file_data)
            head = remote_save_path + "*" + os.path.split(file_save_path)[1] + "*" + str(offset) + "*" + str(
                len(file_data))  # 数据放最后 免得每次+重新分配内存导致的效率低
            protocol_up["data"]["head"] = head
            protocol_up["data"]["content"] = file_data

            self.request_server(client, protocol_up)
            tuple_params = (file_save_path, remote_save_path, offset, size)
            self.deal_server_response_datas(client, tuple_params)
        uf.close()

    def thread_upload_file(self, data, client, args):
        """
        本地文件上传
        :param args: 上传文件的 本地 存储路径, 要上传到服务器上的路径, 读取起始地址, 待上传大小
        :param data: None(第一次读) 或者 结果("SUCCESS")or"(FAILE)*收到的文件大小
        :return:
        """
        code_format = ""  # 编码格式
        file_save_path = str(args[0])
        # print("要上传文件的名称:", file_save_path)
        remote_save_path = str(args[1])
        # print("远程存储路径:", remote_save_path)
        offset = int(args[2])
        size = int(args[3])
        # print("偏移量: %d 待传大小 %d" % (offset, size))

        if data.startswith("SUCCESS"):
            # print("目前的编码格式:", code_format)
            result, server_get_length = data.strip().split("*")
            # print("上传的文件大小:", int(server_get_length))
            offset += int(server_get_length)
            if result == "SUCCESS":
                if int(server_get_length) == size:
                    common_func.progress_bar(self.upload_section, 4, self.upload_section_size, self.upload_section_size)
                    print("\033[33;1m上传完成\033[0m")
                else:
                    common_func.progress_bar(self.upload_section, 4, offset - self.upload_offset, self.upload_section_size)
                    uf = open(file_save_path, "rb")
                    if uf.readable():
                        uf.seek(offset, 0)
                        protocol_up["account"] = RoleBase.RoleBase.account_id
                        protocol_up["password"] = RoleBase.RoleBase.account_pwd
                        protocol_up["cmd"] = "uploading"
                        size -= int(server_get_length)
                        if size > 5 * 1024:
                            file_data = uf.read(5 * 1024)  # 一次读2K
                        else:
                            file_data = uf.read(size)  # 一次读 size
                        # length = len(file_data)
                        # file_data = file_data.decode("utf-8")  # 这个方法并不稳定,建议少用!
                        # print(type(file_data))
                        # print(file_data)
                        head = remote_save_path + "*" + os.path.split(file_save_path)[1] + "*" + str(offset) + "*" + str(len(file_data))
                        protocol_up["data"]["head"] = head
                        protocol_up["data"]["content"] = file_data
                        self.request_server(client, protocol_up)
                        file_params = (file_save_path, remote_save_path, offset, size)
                        tuple_params = (client, file_params,)
                        return tuple_params
                        # self.deal_server_response_datas(client, tuple_params)
                    uf.close()
            elif result == "FAILE":
                print("上传失败")
        else:
            print("***调用记录方法***记录到上传文件信息记录文件,用于断点续传")

    def thread_down_file(self, data, client, args):
        """
        远程服务器文件本地下载写
        :param data: 文件数据 or "FAILE*
        :param client: client
        :param args: 服务器文件路径, 本地存储下载文件的路径, 下载起始偏移量, 待下载文件大小
        :return:
        """
        down_result = 0
        file_remote_save_path = args[0]
        local_path = args[1]
        tmp_local_path = local_path + ".tmp"
        offset = int(args[2])
        remain_size = int(args[3])  # 剩余下载大小
        protocol["account"] = RoleBase.RoleBase.account_id
        protocol["password"] = RoleBase.RoleBase.account_pwd
        protocol["cmd"] = "downloading"
        if not data:
            pass
        else:
            if data != "FAILE":
                # recv_data = b''
                recv_data = data
                recv_data_size = len(recv_data)
                # print("下载路径:", file_remote_save_path)
                # print("写入%s" % local_path)
                # print("接收到的数据大小:---------------", recv_data_size)
                # os.chmod(local_path, stat.S_IRWXG)  # 写之前更改写入权限

                with open(tmp_local_path, "ab") as f:  # 写本地存储文件,这里有有个坑，最好以管理员身份运行，要不然可能会报错：提示没有权限写
                    # print(type(recv_data))
                    # print("写文件的数据是:", recv_data)
                    # print("写入起始位置:", offset)
                    # print(f.tell())
                    f.seek(offset, 0)
                    # print(f.tell())
                    f.write(recv_data)

                if remain_size >= recv_data_size:
                    remain_size -= recv_data_size

                if remain_size == 0:
                    common_func.progress_bar(self.download_section, 4, self.download_section_size, self.download_section_size)
                    print("下载完成了!")
                    if self.download_section == 4:
                        os.rename(tmp_local_path, local_path)
                else:
                    common_func.progress_bar(self.download_section, 4, offset - self.download_offset,
                                             self.download_section_size)
                    # print("剩余下载大小:", remain_size)
                    offset += recv_data_size
                    self.write_download_record(local_path, offset, file_remote_save_path)
                    request_size = 0
                    if remain_size > 10 * 1024:
                        request_size = 10 * 1024
                    else:
                        request_size = remain_size
                    # print("请求下载大小", request_size)
                    protocol["data"] = file_remote_save_path + "*" + str(offset) + "*" + str(request_size)
                    # s = RequestTask(client, protocol)
                    # request_send_queue.put(s)
                    self.request_server(client, protocol)
                    # t = threading.Thread(target=self.request_server, args=(client, protocol,))
                    # t.start()
                    # t.join()
                    file_params = (file_remote_save_path, local_path, offset, remain_size,)
                    tuple_params = (client, file_params,)
                    return tuple_params
                # self.deal_server_response_datas(client, tuple_params)
            else:
                protocol["data"] = "FAILE" + "0"
                print("下载失败")
                down_result = -1

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

    def write_download_record(self, local_path, now_size, remote_path):
        """下载记录保存
        :param local_path: 本地下载文件存储地址
        :param now_size: 偏移量
        :param remote_path: 服务器文件存储地址
        :now_size: 偏移量
        """
        # print("记录下载情况")
        record_path = settings.source_dist.get("download_record_dir") + os.sep + RoleBase.RoleBase.account_id
        # print("record_path", record_path)
        record_info = dict(zip(User.upload_protocol, (local_path, now_size, remote_path)))
        if not os.path.exists(record_path):
            with open(record_path, "w+") as wc:
                pass
        else:
            with open(record_path, "r") as rf, \
                    open(record_path + '.tmp', "w") as wf:  # 修改下载记录文件
                    data = rf.readline()
                    if not data:
                        reocrd_datas = record_info
                    else:
                        reocrd_datas = eval(data)
                    if reocrd_datas.get("local_path") == local_path:
                        reocrd_datas["offset"] = now_size
                    else:
                        reocrd_datas = record_info
                    wf.writelines(str(reocrd_datas) + "\n")
                    wf.flush()
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
