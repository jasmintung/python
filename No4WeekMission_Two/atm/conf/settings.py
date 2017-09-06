import os
import logging
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOG_LEVEL = logging.INFO
LOG_TYPES = {
    "transaction": "transactions.log",
    "access": "access.log"
}
DATABASE = {
    'engine': 'file_storage',
    'name': 'accounts',
    'path': "%s/db" % BASE_DIR
}
# 下面定义的是支持的交易类型(取现, 转账, 还款, 消费)
TRANSACTION_TYPE = {
    "cash_out": {"action": "minus", "interest": 0.05},
    "transfer": {"action": "minus", "interest": 0.05},
    "repay": {"action": "plus", "interest": 0},
    "consume": {"action": "minus", "interest": 0}
}