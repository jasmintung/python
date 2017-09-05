from conf import settings
from core import logger
from core import accounts


def admin_operation(log_obj, operation_type, account_id, account_data, *others):
    """
    管理员操作接口
    :param log_obj:
    :param operation_type:
    :param account_id:
    :param account_data:
    :return:
    """
    if operation_type == 1:
        return accounts.add_account(account_id, account_data)
    elif operation_type == 2:
        current_credit = account_data["credit"]
        print(others[0], current_credit, account_data["balance"])
        if int(others[0]) > current_credit:  # 额度调高了
            account_data["balance"] = int(others[0]) - current_credit + account_data["balance"]
        else:
            if account_data["balance"] > others[0]:
                account_data["balance"] = others[0]
        account_data["credit"] = int(others[0])
        return accounts.dump_account(account_data)  # save the new balance back to file
    elif operation_type == 3:
        account_data["status"] = 1
        return accounts.dump_account(account_data)  # save the new balance back to file
