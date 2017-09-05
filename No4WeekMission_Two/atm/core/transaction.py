from conf import settings
from core import accounts
from core import logger


def make_transaction(log_obj, account_data, tran_type, amount, **other):
    """
    deal all the user transcations
    :param log_obj: 日志记录
    :param account_data: user account data
    :param tran_type: transaction type
    :param amount: transaction amount
    :param other: for loggin usage
    :return:
    """

    amount = float(amount)
    new_balance = 0.0
    if tran_type in settings.TRANSACTION_TYPE:
        interest = amount * settings.TRANSACTION_TYPE[tran_type]["interest"]  # 手续费
        old_balance = account_data["balance"]  # 当前可用额度
        if settings.TRANSACTION_TYPE[tran_type]["action"] == "plus":
            new_balance = old_balance + amount + interest
        elif settings.TRANSACTION_TYPE[tran_type]["action"] == "minus":
            new_balance = old_balance - amount - interest
            # check credit
            if new_balance < 0:
                print("""\033[31;1m Your credit [%s] is not enough for this transaction [-%s], your current balanc is 
                [%s]""" % (account_data["credit"], (amount + interest), old_balance))
                return
        account_data["balance"] = new_balance
        accounts.dump_account(account_data)  # save the new balance back to file
        # 记录日志

        return account_data
    else:
        print("\033[31;1m Transaction type [%s] is not exist!\033[0m" % tran_type)