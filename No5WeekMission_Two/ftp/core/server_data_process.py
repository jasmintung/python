import os
import json
from conf import settings
db_dir = settings.DATABASE


class ServerDataProcess(object):

    def __init__(self):
        self.data = ""
        self.protocol = {
            "account": "",
            "password": "",
            "cmd": "",
            "data": 0}

    def set_process_res_data(self, args):
        return args

    def get_process_res_data(self):
        return self.protocol

    def analyse_client_data(self, args):
        recv_data = eval(args.decode())
        if isinstance(recv_data, dict):
            if recv_data["cmd"] == "login":
                self.process_login(recv_data.get("account"), recv_data.get("password"))
            elif recv_data["cmd"] == "view":
                self.process_view(recv_data.get("account"), recv_data.get("password"))
            elif recv_data["cmd"] == "next":
                self.process_next(recv_data.get("account"), recv_data.get("password"), recv_data.get("data"))
            elif recv_data["cmd"] == "prev":
                self.process_prev(recv_data.get("account"), recv_data.get("password"), recv_data.get("data"))
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

    def process_next(self, account, password, path):
        check_result = self.account_check(account, password)
        current_path = check_result[1]

    def process_prev(self, account, password, path):
        pass

    def process_download(self, account, password, download_file_path):
        pass

    def process_download_res(self, account, password, response):
        pass

    def process_download_ing(self, account, password, down_file_data):
        pass

    def process_upload(self, account, password, args):
        pass

    def process_upload_res(self, account, password, response):
        pass

    def process_upload_ing(self, account, password, upload_file_data):
        pass
