import random, time
from core import db_handler


def auth_code():
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


def login_required(func):
    """
    验证用户是否登录装饰器
    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        if args[0].get("is_authenticated"):
            return func(*args, **kwargs)
        else:
            exit("User is not authenticated.")
    return wrapper


def acc_auth(account, password):
    """
    认证接口
    :param account: credit account number
    :param password: credit card password
    :return: if passed the authentication, return the account object, otherwise, return None
    """
    db_api = db_handler.db_handler()
    data = db_api("select * from accounts where account=%s" % account)  # 将当前账号信息json格式返回

    if data['password'] == password and data['status'] == 0:
        exp_time_stamp = time.mktime(time.strptime(data['expire_date'], "%Y-%m-%d"))  # 返回时间戳
        if time.time() > exp_time_stamp:  # 账户过期
            print("\033[31;1mAccount [%s] has expired, please contact the bank to get new card!\033[0m" % account)
        else:
            return data
    else:
        if data['status'] == 1:
            print("\033[31;1m您的账户被冻结了!\033[0m")
        else:
            print("\033[31;1m用户名或者密码不正确!\033[0m")


def login(user_data, log_obj):
    """
    account login func
    :param user_data: user info data, only saves in memory
    :param log_obj:
    :return:
    """
    retry_count = 0
    while user_data['is_authenticated'] is not True and retry_count < 5:
        account = input("\033[32;1maccount:\033[0m").strip()
        password = input("\033[32;1mpasword:\033[0m").strip()

        if retry_count > 2:
            print("验证码:\033[35;1m %s \033[0m" % auth_code())
            enter_auth_code = input("请输入验证码")
            if enter_auth_code != auth_code().strip():
                print("输入错误!")
                continue
        auth = acc_auth(account, password)
        if auth:
            user_data['is_authenticated'] = True
            user_data['account_id'] = account
            print("Welcome!")
            return auth
        retry_count += 1

    else:
        # 日志记录,并锁定账户
        log_obj.error("account [%s] too many login attempts.SO LOCK!" % account)
        print("lock this account!")
        exit()
