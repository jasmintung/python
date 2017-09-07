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

    if sql_list[0].startswith("select") and len(sql_list[0]) > 1:
        print("select db!!!")
        column, val = sql_list[1].strip().split("=")
        if column == "account":
            account_file = "%s/%s.json" % (db_path, val)  # 得到当前用户的账户信息json文件名
            print(account_file)
            if os.path.isfile(account_file):
                with open(account_file, "r") as rf:
                    account_data = json.load(rf)
                    return account_data
            else:
                print("\033[31;1m账户 [%s] 未注册!\033[0m" % val)
    elif sql_list[0].startswith("update") and len(sql_list[0]) > 1:
        print("update db!!!")
        column, val = sql_list[1].strip().split("=")
        if column == "account":
            account_file = "%s/%s.json" % (db_path, val)
            if os.path.isfile(account_file):
                account_data = kwargs.get("account_data")
                with open(account_file, "w") as wf:
                    json.dump(account_data, wf)
                return True
            else:
                return False
    elif sql_list[0].startswith("insert") and len(sql_list[0]) > 1:
        print("db insert!!!!!")
        start_index = int(sql_list[0].find("insert")) + 12
        end_index = int(sql_list[0].find("values")) - 1
        name = sql_list[0][start_index:end_index]
        print(name)
        account_file = "%s/%s.json" % (db_path, name)
        if os.path.exists(account_file):  # 已经存在,就不添加了
            return False
        else:
            account_data = kwargs.get("account_data")
            print(account_data)
            with open(account_file, "w") as wf:
                json.dump(account_data, wf)
            return True

    else:
        print("不支持这个操作!")