from core import common_func
from conf import settings
import os
protocol = {"account": "", "password": "", "cmd": "", "data": ""}


def login(auth_type):
    def auth(func):
        def inner(self, *args, **kwargs):
            go_next = False
            if auth_type == 'admin':
                pass
            elif auth_type == 'user':
                pass
            elif auth_type == 'request':
                pass
            else:
                print("not support this login type")
            if go_next:
                retry_count = 0
                is_login_statue = -1
                account = ""
                while retry_count < 5:
                    account = input("\033[32;1m用户名:\033[0m").strip(">>")
                    password = input("\033[32;1m密码:\033[0m").strip(">>")
                    if account == 'b' or password == 'b':
                        exit()
                    if retry_count > 2:
                        print("验证码:\033[35;1m %s \033[0m" % common_func.auth_code())
                        enter_auth_code = input("请输入验证码").strip(">>")
                        if enter_auth_code != common_func.auth_code().strip():
                            print("输入错误!")
                            retry_count += 1
                            continue
                    if auth_type == 'request':
                        self.set_account(account, password)
                        func(*args, **kwargs)
                        recv_data = self.conn.get_response()
                        cmd, value = self.analysis_protocol(recv_data)
                        if cmd == "login":
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
                        """服务器端处理"""
                        pass
                else:
                    # 日志记录,并强制退出
                    exit("\033[32;1m您尝试登陆次数过多,被强制踢出!\033[0m")
                    self.update_login_statue(False)
        return inner
    return auth


class RoleBase(object):
    """角色基类"""
    account_dir = settings.source_dist.get("account_path")
    account_id = ""  # 用户ID
    account_pwd = ""  # 用户密码
    home_dir = ""  # 默认用户home目录绝对路径
    login_statue = 0  # 登陆状态

    def __init__(self, conn):
        self.is_login = False
        self.conn = conn
        self.cur_dir = ""  # 当前用户访问的目录绝对路径,根据需求要求的权限设定: 一定是以home目录开始的字符串
        self.dir_files = ""  # 路径下的文件及文件夹及子目录名集合,通过','号隔开

    @login('request')
    def request_auth(self, role_type):
        protocol["account"] = RoleBase.account_id
        protocol["password"] = RoleBase.account_pwd
        protocol["cmd"] = "login"
        protocol["data"] = role_type
        self.conn.send_request(protocol)

    @login('admin')
    def a_auth(self):
        admin_dir = ""
        admin_dir = RoleBase.account_dir + settings.source_dist.get("admin_pack_name")
        admin_path = ""
        admin_path = admin_dir + self.account_id
        return self.account_check(admin_path)

    @login('user')
    def u_auth(self):
        user_dir = ""
        user_dir = RoleBase.account_dir + settings.source_dist.get("user_pack_name")
        user_path = ""
        user_path = user_dir + self.account_id
        return self.account_check(user_path)

    def account_check(self, path):
        if os.path.exists(path) is False:
            """账户不存在"""
            return 0
        else:
            if os.path.isfile(path):
                pass
            else:
                """账户异常"""
                return -1

    def analysis_protocol(self, args):
        recv_datas = b''
        if len(args) > 0:
            recv_datas = eval(str(args.decode()))
            return recv_datas.get("cmd"), recv_datas.get("data")

    def update_login_statue(self, args):
        """更新用户登陆状态"""
        self.is_login = args

    def get_login_statue(self):
        """获取用户登陆状态"""
        return self.is_login

    def set_default_home_path(self, args):
        """设置用户默认home路径"""
        RoleBase.home_dir = args

    def get_default_home_path(self):
        """获取用户默认home路径"""
        return RoleBase.home_dir

    def set_dir_files(self, args):
        """保存当前路径下的所有子目录及文件名"""
        self.dir_files = args

    def get_dir_files(self):
        """获取当前路径下的所有子目录及文件名"""
        return self.dir_files

    def set_account(self, uid, password):
        RoleBase.account_id = uid
        RoleBase.account_pwd = password
