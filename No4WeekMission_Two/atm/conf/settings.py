import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DATABASE = {
    'engine': 'file_storage',
    'name': 'accounts',
    'path': "%s/db" % BASE_DIR
}
# 下面定义的是支持的交易类型(取现, 转账, 还款, 消费)
TRANSACTION_TYPE = {
    "cash_out": {"action": "minus"},
    "transfer": {"action": "minus"},
    "repay": {"action": "plus"},
    "consume": {"action": "minus"}
}