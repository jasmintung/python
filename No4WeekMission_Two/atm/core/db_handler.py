import os, json
from conf import settings


def file_db_handler(conn_params):
    """
    parse the db file path
    :param conn_params: the db connection params set in settings
    :return:
    """
    print("file db:", conn_params)
    return file_execute


def db_handler():
    """
    connect to db
    :return:
    """
    conn_params = settings.DATABASE
    if conn_params['engine'] == 'file_storage':
        return file_db_handler(conn_params)
    elif conn_params['engine'] == 'mysql':
        pass


def file_execute(sql, **kwargs):
    conn_params = settings.DATABASE
    db_path = "%s/%s" % (conn_params['path'], conn_params['name'])
    print(sql, db_path)
    sql_list = sql.split("where")
    print(sql_list)
    if sql_list[0].startswith("select") and len(sql_list) > 1:
        column, val = sql_list[1].strip().split("=")
        if column == "account":
            account_file = "%s/%s.json" % (db_path, val)  # 得到当前用户的账户信息json文件名
            print(account_file)
            if os.path.isfile(account_file):
                with open(account_file, "r") as rf:
                    account_data = json.load(rf)
                    return account_data
            else:
                exit("\033[31;1mAccount [%s] does not exist!\033[0m" % val)