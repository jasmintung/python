# __author__:"zhangtong"
from core import auth
from core.auth import login_required
from core import accounts
from core import transaction
from core import operation

import time, datetime

# temp account data, only save the data in memory
user_data = {
    'account_id': None,
    'is_authenticated': False,
    'account_data': None
}

account_dict = {
  "balance": None,
  "expire_date": None,
  "enroll_date": None,
  "credit": 0,
  "id": 0,
  "status": 0,
  "pay_day": 0,
  "password": None
}


def add_user():
    """
    管理员功能添加账户,ID与用户名保持一致
    """
    print("管理员添加账户业务")
    account_name = input("请输入存档用户名")
    id = input("输入账户ID")
    pwd = input("输入账户密码")
    expire_data = input("输入账户有效期:20xx-xx-xx")
    pay_day = int(input("输入还款日(0~28)"))
    credit = int(input("请输入额度:"))
    enroll_date = datetime.date.fromtimestamp(time.time())  # 登记时间
    account_dict["balance"] = credit
    account_dict["expire_date"] = expire_data
    account_dict["enroll_date"] = str(enroll_date)
    account_dict["credit"] = credit
    account_dict["id"] = id
    account_dict["status"] = 0
    account_dict["pay_day"] = pay_day
    account_dict["password"] = pwd
    operation.admin_operation(0, 1, account_name, account_dict)


def adjust_user_balance():
    """
    管理员功能调整用户额度
    :return:
    """
    r_flag = False

    while not r_flag:
        print("额度调整--->输入字符'b'退出")
        account_id = input("请输入要调整的账户ID")
        account_data = accounts.load_current_balance(account_id)
        current_balance = """ --------BALANCE INFO -----------
            Credit :    %s
            Balance  :  %s
            """ % (account_data['credit'], account_data['balance'])  # 额度 和 可用额度
        print(current_balance)

        adjust_balance = int(input("输入调整额度(整数):"))
        if adjust_balance > 0:
            new_balance = operation.admin_operation(0, 2, account_id, account_data, adjust_balance)
            if new_balance is True:
                print("\033[31;1m调整成功!\033[0m")
            else:
                print("\033[31;1m调整失败!\033[0m")
        if adjust_balance == 'b':
            r_flag = True


def cool_user_account():
    """
    管理员功能冻结账户
    :return:
    """
    r_flag = False
    while not r_flag:
        print("冻结账户,谨慎操作--->输入字符'b'退出")
        account_id = input("请输入要冻结的账户ID")
        account_data = accounts.load_current_balance(account_id)
        current_balance = """ --------BALANCE INFO -----------
            Credit :    %s
            Balance  :  %s
            """ % (account_data['credit'], account_data['balance'])  # 额度 和 可用额度
        print(current_balance)
        cool_account = operation.admin_operation(0, 3, account_id, account_data)
        if cool_account is True:
            print("\033[41;1m冻结账户成功!\033[0m")
        else:
            print("\033[31;1m冻结账户失败!\033[0m")
        if account_id == 'b':
            r_flag = True


def account_info(acc_data):
    account_data = accounts.load_current_balance(acc_data['account_id'])
    info = """
    ******************%s 账户信息*******************
    \033[28;1mID: %s
    额度: %s
    可用额度: %s
    有效期: %s\033[0m
    **********************************************
    """ % (account_data['id'], account_data['id'], account_data['credit'], account_data['balance'], account_data['expire_date'])
    print(info)


@login_required
def cash_out(acc_data):
    print("提现业务")
    account_data = accounts.load_current_balance(acc_data['account_id'])
    current_balance = """ --------BALANCE INFO -----------
    Credit :    %s
    Balance  :  %s
    """ % (account_data['credit'], account_data['balance'])  # 额度 和 可用额度
    print(current_balance)
    r_flag = False
    while not r_flag:
        cash_need = input("\033[33;1mInput need cash mounts: \033[0m").strip()
        if len(cash_need) > 0:
            new_balance = transaction.make_transaction(0, account_data, "cash_out", cash_need)
            if new_balance:  # 提现成功
                print("提现成功!")
                print("""\033[41;1m New Balance%s\033[0m""" % new_balance["balance"])
                r_flag = True
            else:
                print("\033[31;1m cash out failed!\033[0m")
        else:
            print("\033[31;1m[%s] is not valid amount, only accept integer!\033[0m" % cash_need)
        if cash_need == 'b':
            r_flag = True


@login_required
def transfer(acc_data):
    print("转账业务")
    account_data = accounts.load_current_balance(acc_data['account_id'])
    current_balance = """ --------BALANCE INFO -----------
        Credit :    %s
        Balance  :  %s
        """ % (account_data['credit'], account_data['balance'])  # 额度 和 可用额度
    print(current_balance)
    bak_account_balance = account_data['balance']
    r_flag = False
    while not r_flag:
        transfer_amount = input("\033[33;1m输入转账金额: \033[0m").strip()  # 转账金额
        to_account = input("\033[33;1m转入账户ID: \033[0m").strip()  # 接收账户----account_id
        tmp_to_account_balance = 0
        if len(transfer_amount) > 0:
            new_balance = transaction.make_transaction(0, account_data, "transfer", transfer_amount)  # 转账账户先扣款
            if new_balance:  # 扣款成功后,收款账户进账
                print("""\033[41;1mNew Balance:%s\033[0m""" % new_balance["balance"])
                tmp_to_account_balance = new_balance["balance"]
                to_account_data = accounts.load_current_balance(to_account)
                if to_account_data:
                    to_account_balance = """---------- TO BALANCE INFO ----------
                    Credit : %s
                    Balance : %s
                    """ % (to_account_data["credit"], to_account_data["balance"])
                    print(to_account_balance)

                    # 调用还款接口进行转账业务给指定账户
                    to_new_balance = transaction.make_transaction(0, to_account_data, "repay", transfer_amount)
                    if to_new_balance:
                        print("""\033[41;1mTo New Balance:%s\033[0m""" % to_new_balance["balance"])
                        r_flag = True
                        break
            transaction.make_transaction(0, account_data, "repay",
                                         bak_account_balance - tmp_to_account_balance)  # 转账失败撤回资金
            r_flag = True
            print("\033[31;1mtransfer failed!\033[0m")

        else:
            print("\033[31;1mamount must bigger than zero!\033[0m")
        if transfer_amount == 'b' or to_account == 'b':
            r_flag = True


@login_required
def repay(acc_data):
    print("还款业务")
    account_data = accounts.load_current_balance(acc_data['account_id'])
    current_balance = """ --------BALANCE INFO -----------
            Credit :    %s
            Balance  :  %s
            """ % (account_data['credit'], account_data['balance'])  # 额度 和 可用额度
    print(current_balance)
    r_flag = False
    while not r_flag:
        payments = input("\033[33;1mInput payments: \033[0m").strip()  # 还款金额
        # 后期可考虑加一层关联还款方式
        if len(payments) > 0:
            new_balance = transaction.make_transaction(0, account_data, "repay", payments)
            if new_balance:
                print("""\033[41;1m New Balance:%s\033[0m""" % new_balance["balance"])
                r_flag = True
            else:
                print("\033[31;1m repay failed!\033[0m")
        else:
            print("\033[31;1m payments is valid\033[0m")
        if payments == 'b':
            r_flag = True


def search_consumption_record(*acc_data):
    """
    查询消费记录接口
    :return:
    """
    print("查询消费记录")


def end(*acc_data):
    exit("退出了!")


def admin_control():
    """
    admin functions
    :return:
    """
    menu = u'''
    \033[32;1m 选择操作:
    1.添加账户
    2.调整额度
    3.冻结账户
    4.查询
    5.结束
    \033[0m
    '''

    menu_dic = {
        "1": add_user,
        "2": adjust_user_balance,
        "3": cool_user_account,
        "4": search_consumption_record,
        "5": end
    }
    exit_flag = False
    while not exit_flag:
        print(menu)
        choice = input("请选择:").strip("<<")
        if choice in menu_dic:
            menu_dic[choice]()
        else:
            print("\033[31;1mOption does not exist!\033[0m")


def interactive(acc_data):
    """
    interact with user
    :param acc_data:
    :return:
    """
    menu = u'''
    \033[32;1m
    1. 账户信息
    2. 提现
    3. 转账
    4. 还款
    5. 查询消费记录
    6. 退出
    \033[0m
    '''
    # print(menu)
    menu_dic = {
        "1": account_info,
        "2": cash_out,
        "3": transfer,
        "4": repay,
        "5": search_consumption_record,
        "6": end
    }
    exit_flag = False
    while not exit_flag:
        print(menu)
        user_option = input(">>").strip()
        if user_option in menu_dic:
            menu_dic[user_option](acc_data)
        else:
            print("\033[31;1mOption does not exist!\033[0m")


def run():
    args = ""  # 日志对象
    welcome_info = """
    -------------------ST HAPPY Bank-----------------
    Welcome!
    """
    print(welcome_info)
    charactor = int(input("0:管理员 还是 1:普通用户? 请选择: "))
    if charactor == 0:
        """
        用户名,密码固定,admin, 988123
        """
        r_flag = False
        while not r_flag:
            print("\033[5;33;1m--->输入字符'b'退出!\033[0m")
            user_name = input("输入用户名:").strip(">>")
            user_pwd = input("输入密码:").strip(">>")
            if user_pwd == 'b' or user_name == 'b':
                exit("退出了!")
            else:
                if user_name.strip() == "admin" and user_pwd == "988123":
                    admin_control()

    elif charactor == 1:
        acc_data = auth.login(user_data, args)
        if user_data['is_authenticated']:
            user_data['account_data'] = acc_data
            interactive(user_data)


