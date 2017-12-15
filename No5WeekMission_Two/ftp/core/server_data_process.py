import os
import json
from conf import settings
db_dir = settings.DATABASE


class ServerDataProcess(object):

    def __init__(self, socket):
        self.socket = socket
        self.data = ""
        self.current_download_path = ""
        self.protocol = {
            "account": "",
            "password": "",
            "cmd": "",
            "data": 0}

    def set_process_res_data(self, args):
        return args

    def get_process_res_data(self):
        return self.protocol

    def get_current_download_path(self):
        return self.current_download_path

    def set_current_download_path(self, path):
        self.current_download_path = path

    def analyse_client_data(self, args):
        recv_data = eval(args.decode())
        if isinstance(recv_data, dict):
            if recv_data["cmd"] == "login":
                self.process_login(recv_data.get("account"), recv_data.get("password"))
            elif recv_data["cmd"] == "view":
                self.process_view(recv_data.get("account"), recv_data.get("password"))
            elif recv_data["cmd"] == "jump":
                self.process_next_prev(recv_data.get("account"), recv_data.get("password"), recv_data.get("data"))
            elif recv_data["cmd"] == "download":
                self.process_download(recv_data.get("account"), recv_data.get("password"), recv_data.get("data"))
            elif recv_data["cmd"] == "upload":
                self.process_upload(recv_data.get("account"), recv_data.get("password"), recv_data.get("data"))
            elif recv_data["cmd"] == "download_RES":
                self.process_download_res(recv_data.get("account"), recv_data.get("password"), recv_data.get("data"))
            elif recv_data["cmd"] == "upload_RES":
                self.process_upload_res(recv_data.get("account"), recv_data.get("password"), recv_data.get("data"))
            elif recv_data["cmd"] == "upload_ing":
                self.process_upload_ing(recv_data.get("account"), recv_data.get("password"), recv_data.get("data"))

    def account_check(self, account, password):
        result = 0
        default_path = ""
        user_db_path = "%s/%s" % (db_dir.get("dir"), account)
        if os.path.isfile(user_db_path) and os.path.exists(user_db_path):
            print("账户存在")
            with open(user_db_path, "r", encoding="utf-8") as rf:
                account_dict = json.load(rf)
                if account_dict.get("password") != password:
                    print("密码错误!")
                    result = 8
                else:
                    access = account_dict.get("authentication")
                    default_path = account_dict.get("path")
                    if access == "Real":
                        result = 1
                    elif access == "Guest":
                        result = 2
                    elif access == "Admin":
                        result = 9
                    else:
                        print("未知权限")
        else:
            print("用户不存在！")
            result = 0
        return result, default_path

    def process_login(self, account, password):
        check_result = self.account_check(account, password)
        response_dict = {}
        response_dict["account"] = account
        response_dict["password"] = password
        response_dict["cmd"] = "login"
        response_dict["data"] = check_result[0]
        self.set_process_res_data(response_dict)

    def process_view(self, account, password):
        check_result = self.account_check(account, password)
        file_list = os.listdir(check_result[1])  # 这里返回的是一个列表
        response_dict = {}
        response_dict["account"] = account
        response_dict["password"] = password
        response_dict["cmd"] = "login"
        response_dict["data"] = check_result[1] + "*" + "".join(file_list)
        self.set_process_res_data(response_dict)

    def process_next_prev(self, account, password, jump_path):
        response_dict = {}
        response_dict["account"] = account
        response_dict["password"] = password
        response_dict["cmd"] = "jump"
        default_path = ""
        check_result = self.account_check(account, password)
        result = check_result[0]
        default_path = check_result[1]
        if result != 0 and result != 8:
            response_dict["data"] = self.target_path_check(result, account, default_path, jump_path)
        self.set_process_res_data(response_dict)

    def process_download(self, account, password, download_file_path):
        response_dict = {}
        response_dict["account"] = account
        response_dict["password"] = password
        response_dict["cmd"] = "download_RES"
        if not os.path.isfile(download_file_path):
            response_dict["data"] = "file_not_exists"
        else:
            check_result = self.account_check(account, password)
            result = check_result[0]
            default_path = check_result[1]
            if result != 0 and result != 8:
                response_dict["data"] = self.target_file_check(result, account, default_path, download_file_path)
        self.set_process_res_data(response_dict)

    def process_download_res(self, account, password, response):
        if response == "READY":
            response_dict = {}
            response_dict["account"] = account
            response_dict["password"] = password
            response_dict["cmd"] = "download_ing"
            file_path = self.get_current_download_path()
            fp = open(file_path, "rb")
            while True:
                file_data = fp.read(1*1024)
                response_dict["data"] = file_data
                if not file_data:
                    break
                self.socket.send(response_dict)
            self.socket.close()
            print("send over...")

    def process_upload(self, account, password, args):
        pass

    def process_upload_res(self, account, password, response):
        pass

    def process_upload_ing(self, account, password, upload_file_data):
        pass

    # 这里有个规则,管理员创建用户目录的时候，所有用户的目录都在同一个父目录下面

    def target_path_check(self, account_type, account, default_path, target_path):
        result_data = ""
        if os.path.isdir(target_path):  # 先判断要跳转的路径是否存在
            # 接着判断根路径是否一致,否则跳转到其它根去了是不允许的
            index = default_path.find(":")
            base_dir = default_path[0:index+1]
            if target_path.startwith(base_dir):
                # 接着判断要跳转的路径是否是其它用户的目录里面去了:F:\mnt\streamax\home\zhangtong
                user_content_base = default_path[0:default_path.find(account)]  # 得到 F:\mnt\streamax\home\
                user_content1 = default_path[default_path.find(account):-1]  # 得到上面目录 zhangtong在字符串的坐标
                if target_path.startwith(user_content_base):
                    if len(default_path) < len(target_path):
                        if target_path.find(user_content_base) != -1:
                            target_user_content1 = target_path[len(user_content_base):-1]
                            if not target_user_content1.startwith(user_content1):
                                if account_type == 1:  # Real用户不能访问同级目录的其它用户的目录及文件内容
                                    result_data = "no_permission"
                                elif account_type == 9:  # 管理员可以访问
                                    print("可以访问拉!")
                                    result_data = target_path + "*" + "".join(os.listdir(target_path))
                            else:
                                if account_type == 2:
                                    print("可以访问拉!")
                                    result_data = target_path + "*" + "".join(os.listdir(target_path))
                        else:
                            result_data = "path_error"
                    else:
                        if len(target_path) > len(user_content_base):
                            # F:\mnt\streamax\home\zhangtong
                            # target:   F:\mnt\streamax\home\same
                            # target:   F:\mnt\streamax\home\tongzhang
                            target_user_content1 = target_path[len(user_content_base):-1]
                            if user_content1 != target_user_content1:
                                if account_type == 1:  # Real用户不能访问同级目录的其它用户的目录及文件内容
                                    result_data = "no_permission"
                                elif account_type == 9:  # 管理员可以访问
                                    print("可以访问拉!")
                                    result_data = target_path + "*" + "".join(os.listdir(target_path))
                            else:

                                print("可以访问拉!")
                                result_data = target_path + "*" + "".join(os.listdir(target_path))
                        else:
                            # F:\st\workspace
                            if account_type != 2:
                                print("可以访问拉!")
                                result_data = target_path + "*" + "".join(os.listdir(target_path))
                            else:
                                result_data = "no_permission"
                else:
                    if account_type != 2:
                        print("可以访问拉!")
                        result_data = target_path + "*" + "".join(os.listdir(target_path))
                    else:
                        result_data = "no_permission"
            else:
                result_data = "path_error"
        else:
            result_data = "path_error"
        return result_data

    def target_file_check(self, account_type, account, default_path, target_file):
        # 下载路径的检查比较简单,判断下载路径是否是在初始路径下的子目录中的文件即可,或者下载路径在根路径下的其它目录中的文件并且不是其它用户目录下的文件
        result_data = ""
        user_account = default_path[default_path.find(account):-1]  # 再加一个账户验证
        user_content_base = default_path[0:default_path.find(account)]
        if user_account != account:
            result_data = "file_not_exists"
        else:
            if target_file.startwith(default_path):
                if os.path.exists(target_file):
                    result_data = os.path.getsize(target_file)
                    self.set_current_download_path(target_file)
                else:
                    result_data = "file_not_exists"
            else:
                if target_file.startwith(user_content_base):
                    temp_sub_path = target_file[default_path.find(account):-1]
                    if not temp_sub_path.startwith(account):
                        result_data = "file_not_exists"
                    else:
                        result_data = os.path.getsize(target_file)
                        self.set_current_download_path(target_file)
        return result_data