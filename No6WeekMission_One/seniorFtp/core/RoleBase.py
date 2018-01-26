from core import common_func


class RoleBase(object):
    """角色基类"""
    def __init__(self):
        self.is_login = False
        self.account_id = ""
        self.account_pwd = ""

    def auth(self):
        """
        加密认证
        :return: 认证结果
        """
        result = False
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
            # is_login_statue = self.acc_auth(account, password)
            if is_login_statue == 0:
                print("\033[32;1m登陆成功\033[0m")
                break
            else:
                print("\033[35;1m用户名或密码错误!\033[0m")

        else:
            # 日志记录,并强制退出
            exit("\033[32;1m您尝试登陆次数过多,被强制踢出!\033[0m")
        return result
