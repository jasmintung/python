import random


class AuthModule(object):
    def __init__(self):
        pass

    def auth_code(self):
        """
        生成验证码
        :return: 返回验证码
        """
        checkcode = ""
        for i in range(4):
            current = random.randrange(0, 4)
            if current == i:
                temp = chr(random.randint(65, 90))  # ASCII码转成字符
            else:
                temp = random.randint(0, 9)
            checkcode += str(temp)
        return checkcode

    def acc_auth(self, account, password):
        # 读取账户数据库判断是否有
        return False

    def login(self):
        retry_count = 0
        while retry_count < 5:
            account = input("\033[32;1m用户名:\033[0m").strip(">>")
            password = input("\033[32;1m密码:\033[0m").strip(">>")
            if account == 'b' or password == 'b':
                exit()
            if retry_count > 2:
                print("验证码:\033[35;1m %s \033[0m" % self.auth_code())
                enter_auth_code = input("请输入验证码").strip(">>")
                if enter_auth_code != self.auth_code().strip():
                    print("输入错误!")
                    retry_count += 1
                    continue
            is_login_success = self.acc_auth(account, password)
            if is_login_success:
                print("Welcome!")
                return is_login_success
            else:
                print("\033[36;1m用户名或者密码错误!\033[0m")
            retry_count += 1
        else:
            # 日志记录,并强制退出
            exit()

def login_deco(args):
    # 登陆验证装饰器
    if args == 1:
        def inner_deco(func):
            def wrapper(*args, **kwargs):
                print("亲爱的同学请输入您的用户名和密码")
                func(*args, **kwargs)
            return wrapper
    elif args == 2:
        def inner_deco(func):
            def wrapper(*args, **kwargs):
                print("尊敬的讲师请输入您的用户名和密码")
                func(*args, **kwargs)
            return wrapper
    elif args == 8:
        def inner_deco(func):
            def wrapper(*args, **kwargs):
                print("管理员输入登陆口令")
                func(*args, **kwargs)
            return wrapper
    elif args == 0:
        def inner_deco(func):
            return func
    return inner_deco
