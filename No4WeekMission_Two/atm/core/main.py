# __author__:"zhangtong"
from core import auth
from core.auth import login_required
from core import accounts

# temp account data, only save the data in memory
user_data = {
    'account_id': None,
    'is_authenticated': False,
    'account_data': None
}


def account_info(acc_data):
    print(acc_data)


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
        if len(cash_need) > 0 and cash_out.isdigit():
            pass
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
    r_flag = False
    while not r_flag:
        transfer_amount = input("\033[33;1mInput transfer amount: \033[0m").strip()  # 转账金额
        to_account = input("\033[33;1mInput accept amount: \033[0m").strip()  # 接收账户
        if len(transfer_amount) > 0:
            pass
        else:
            print("\033[31;1m amount must bigger than zero!\033[0m")
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
            pass
        else:
            print("\033[31;1m payments is valid\033[0m")
        if payments == 'b':
            r_flag = True


def search_consumption_record(acc_data):
    print("查询消费记录")


def end():
    exit()


def interactive(acc_data):
    """
    interact with user
    :param acc_data:
    :return:
    """
    menu = u'''
    ---------------- Happy Bnak -------------------
    \033[32;1m
    1. 账户信息
    2. 提现
    3. 转账
    4. 还款
    5. 查询消费记录
    6. 退出
    \033[0m
    '''
    print(menu)
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
        user_option = input(">>").strip()
        if user_option in menu_dic:
            print('accdata', acc_data)
            menu_dic[user_option](acc_data)
        else:
            print("\033[31;1mOption does not exist!\033[0m")


def run():
    args = ""  # 日志对象
    acc_data = auth.login(user_data, args)
    if user_data['is_authenticated']:
        user_data['account_data'] = acc_data
        interactive(user_data)
