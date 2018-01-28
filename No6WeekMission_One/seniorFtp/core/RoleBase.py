from core import common_func
from conf import settings
import os

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
                        pass
                    else:

                        is_login_statue = func(*args, **kwargs)
                        if is_login_statue == 1:
                            print("\033[32;1m登陆成功\033[0m")
                            break
                        elif is_login_statue == 0:
                            print("\033[35;1m账户不存在!\033[0m")
                        elif is_login_statue == -1:
                            print("\033[35;1m账户异常,无法登录,请联系管理员!\033[0m")
                        elif is_login_statue == 2:
                            print("\033[35;1m用户名或密码错误!\033[0m")
                else:
                    # 日志记录,并强制退出
                    exit("\033[32;1m您尝试登陆次数过多,被强制踢出!\033[0m")
        return inner
    return auth

class RoleBase(object):
    """角色基类"""
    acount_dir = settings.source_dist.get("account_path")

    def __init__(self, conn):
        self.is_login = False
        self.account_id = ""
        self.account_pwd = ""
        self.conn = conn

    @login('request')
    def request_auth(self, role_type):
        self.conn.sendall(self.account_id, self.account_pwd, role_type)

    @login('admin')
    def a_auth(self):
        admin_dir = ""
        admin_dir = RoleBase.acount_dir + settings.source_dist.get("admin_pack_name")
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
