import os
import re
import pickle
import json
import shelve

from core import common_func
from core import RoleBase
from conf import settings


def make_dir(path):
    """递归创建目录"""
    if not os.path.isdir(path):
        make_dir(os.path.split(path)[0])
    else:
        return
    os.mkdir(path)


def auth_check_deco(func):
    """登陆状态监测"""
    def wrapper(self, *args, **kwargs):
        if self.login_statue:
            return func(self, *args, **kwargs)
        else:
            print("已经离线通知客户端登陆状态为离线")
    return wrapper


class ShelveUploadRec(object):

    def __init__(self, file_name, size, offset):
        self.file_name = file_name
        self.size = size
        self.offset = offset


class DataCenter(object):
    protocol = ("account", "password", "cmd", "data")

    def __init__(self, conn):
        self.__login_statue = True
        self.upload_file_size = 0
        self.default_path = ""
        self.account = ""
        self.password = ""
        self.conn = conn
        self.retry_login_fail_count = 0  # 后续完善吧
        self.response_data = ""

    def analyse_client_data(self, data):
        # print("服务器收到的数据:")
        recv_data = eval(str(data.decode()))
        if isinstance(recv_data, dict):
            cmd = recv_data.get("cmd")
            print("cmd is :", cmd)
            DataCenter.func_dict.get(cmd)(self, recv_data)

    def account_check(self, data):
        """登陆账户验证"""
        account_id = data.get("account")
        password = data.get("password")
        print("登陆请求用户名: %s, 登陆密码: %s", account_id, password)
        login_statue = 1
        db_dst = "%s%s" % (settings.source_dist.get("account_path") + os.sep, account_id)

        default_path = ""  # 用户在服务器上的home路径
        file_list = ""  # 用户home路径下的文件列表
        print("账户地址:", db_dst)
        if os.path.exists(db_dst):
            with open(db_dst, "rb") as rf:
                account_data = json.load(rf)
                if account_id == account_data.get("id") and password == account_data.get("password"):
                    print("验证通过")
                    default_path = account_data.get("defaultPath")
                    file_list = os.listdir(default_path)
                    self.default_path = default_path
                    self.login_statue = True
                    self.account = account_id
                    self.password = password
                else:
                    if account_data.get("id") != account_id:
                        print("账户异常")  # 文件名跟内部id不一致
                        login_statue = 9
                    else:
                        print("用户名或者密码错误")
                        login_statue = 2
        else:
            login_statue = 0
            print("账户不存在!")
        if login_statue != 1:
            rs_data = dict(zip(DataCenter.protocol, (account_id, password, data.get("cmd"), login_statue)))
        else:
            rs_data = dict(zip(DataCenter.protocol, (account_id, password, data.get("cmd"), str(login_statue) + "*" +
                                                     default_path + "*" + "&".join(file_list))))
        self.set_response_data(rs_data)

    @auth_check_deco
    def view_files(self, data):
        result = ""
        request_view_path = data.get("data")  # 客户端请求访问的路径
        print("客户端请求访问路径", request_view_path)
        print("默认home路径:", self.default_path)
        if request_view_path.startswith(self.default_path):  # 路径或者文件存在
            if os.path.exists(request_view_path):
                if os.path.isfile(request_view_path): # 路径是文件
                    result = "路径不存在"
                else:
                    file_list = os.listdir(request_view_path)
                    result = request_view_path + "*" + "&".join(file_list)
            else:
                result = "路径不存在"
        else:
            result = "没有访问权限"
            print("没有访问权限")
        rs_data = dict(zip(DataCenter.protocol, (self.account, self.password, "view", result)))
        self.set_response_data(rs_data)

    @auth_check_deco
    def process_upload_file_request(self, data):
        result = ""
        account_id = data.get("account")
        request_upload_info = data.get("data")
        print("上传请求消息:", request_upload_info)
        h = re.match("^[A-Za-z](':\'{1}\D+)*(.+)*(\d+)", request_upload_info).group()
        if not h:
            result = "参数有误"
            print("参数有误")
        else:
            if h == request_upload_info:
                save_dir, file_name, file_size = request_upload_info.strip().split("*")
                save_path = save_dir + os.sep + file_name
                if os.path.exists(save_dir + os.sep + file_name):
                    result = "文件已经存在"
                    print("文件已经存在")
                if not os.path.exists(save_dir):
                    if save_dir.startswith(self.default_path):
                        print("初始化服务端存储路径")
                        make_dir(save_dir)
                        with open(save_path, 'wb') as f:  # 创建指定大小的文件
                            pass
                            # f.seek(file_size - 1)
                            # f.write(b'\x00')
                            # f.seek(0, 0)
                        result = "READY"
                    else:
                        result = "参数有误"
                else:
                    with open(save_path, 'wb') as f:  # 创建指定大小的文件
                        pass
                        # f.seek(int(file_size) - 1)
                        # f.write(b'\x00')
                        # f.seek(0, 0)
                        result = "READY"

                    # shelve_dir = settings.source_dist.get("upload_record_path") + os.sep + account_id
                    # os.mkdir(shelve_dir)
                    # up_shv = shelve.open(shelve_dir + os.sep + file_name)  # 持久化序列用于记录上传记录
                    # d = ShelveUploadRec(file_name, file_size, 0)
                    # up_shv["account"] = account_id
                    # up_shv["uprecord"] = d  # 持久化类
                    # up_shv.close()
            else:
                result = "参数有误"
                print("参数有误")
        rs_data = dict(zip(DataCenter.protocol, (self.account, self.password, "upload", result)))
        self.set_response_data(rs_data)

    @auth_check_deco
    def process_uploading_file(self, data):
        result = ""
        write_offset = 0
        account_id = data.get("account")
        write_dir, file_name, offset, write_size, write_data = data.get("data").strip().split("*")
        file_path = write_dir + os.sep + file_name
        print("write_dir: ", write_dir)
        if os.path.isdir(write_dir):
            print("file_path: ", file_path)
            if os.path.isfile(file_path):
                print("服务端写入文件偏移量:", offset)
                print("服务端写入文件数据:", write_data)
                write_data = write_data.encode("utf-8")
                print(type(write_data))
                with open(file_path, "ab") as f: # 上传文件写文件
                    f.seek(int(offset), 0)
                    f.write(write_data)
                write_offset = write_size
                # shelve_dir = settings.source_dist.get("upload_record_path") + os.sep + account_id
                # os.mkdir(shelve_dir)
                # up_shv = shelve.open(shelve_dir + os.sep + file_name, writeback=True)  # 持久化序列用于记录上传记录
                # print(up_shv["account"])
                # print(up_shv["uprecord"])
                # if up_shv["uprecord"].offset <= up_shv["uprecord"].size:
                #     up_shv["uprecord"].offset = write_offset
                # else:
                #     pass
                # up_shv.close()
                result = "SUCCESS" + "*" + str(write_offset)
            else:
                result = "FAILE" + "*" + str(write_offset)
        else:
            result = "FAILE" + "*" + str(write_offset)

        rs_data = dict(zip(DataCenter.protocol, (self.account, self.password, "uploading", result)))
        self.set_response_data(rs_data)

    @auth_check_deco
    def process_download_file_request(self, data):
        result = ""
        request_download_path = data.get("data")
        if os.path.exists(request_download_path):
            if os.path.isfile(request_download_path):
                result = str(os.path.getsize(request_download_path))
            else:
                result = "文件不存在"
        else:
            result = "文件不存在"
        rs_data = dict(zip(DataCenter.protocol, (self.account, self.password, "download", result)))
        self.set_response_data(rs_data)

    @auth_check_deco
    def process_downloading_file(self, data):
        """"服务器下载文件路径"*请求读取文件起始位置*请求大小 or "FAILE*0"""
        result = ""
        request_download_path, offset, download_size = data.get("data").split("*")
        print("请求下载的文件:", request_download_path)
        print("读取文件偏移量:", int(offset))
        print("请求下载大小:", int(download_size))
        download_size = int(download_size)
        if os.path.exists(request_download_path):
            if os.path.isfile(request_download_path):
                with open(request_download_path, "rb") as f:
                    offset = int(offset)
                    f.seek(offset)
                    file_data = f.read(download_size)
                    result = file_data
            else:
                result = "FAILE"
        else:
            result = "FAILE"

        rs_data = dict(zip(DataCenter.protocol, (self.account, self.password, "downloading", result)))
        self.set_response_data(rs_data)

    def set_response_data(self, data):
        self.response_data = data

    def get_response_data(self):
        return self.response_data

    @property
    def login_statue(self):
        return self.__login_statue

    @login_statue.setter
    def login_statue(self, args):
        self.__login_statue = args

    func_dict = {"login": account_check, "view": view_files, "upload": process_upload_file_request,
                 "uploading": process_uploading_file, "download": process_download_file_request,
                 "downloading": process_downloading_file}


