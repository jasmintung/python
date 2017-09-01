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