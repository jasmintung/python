from core import common_func


class DataCenter(object):
    protocol = {"account": "", "password": "", "cmd": "", "data": ""}
    def __init__(self, conn, data):
        self.data = data
        self.account = ""
        self.password = ""
        self.conn = conn
        self.retry_login_fail_count = 0

    def analyse_client_data(self):
        # print("服务器收到的数据:")
        recv_data = eval(self.data.decode())
        if isinstance(recv_data, dict):

    def account_check(self):
        """账户检测"""
        self.set_account(account, password)

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
            break
        elif is_login_statue == '0':
            print("\033[35;1m账户不存在!\033[0m")
            self.update_login_statue(False)
            break
        elif is_login_statue == '9':
            print("\033[35;1m账户异常,无法登录,请联系管理员!\033[0m")
            self.update_login_statue(False)
            break
        elif is_login_statue == '2':
            print("\033[35;1m用户名或密码错误!\033[0m")
            retry_count += 1
        else:
            # 日志记录,并强制退出
            exit("\033[32;1m您尝试登陆次数过多,被强制踢出!\033[0m")
            self.update_login_statue(False)

    func_dict = {"login": account_check, "view": view_files_response, "upload": upload_file_response,
                 "uploading": thread_upload_file, "download": download_file_response,
                 "downloading": thread_down_file}


