import json
from conf import settings


def write_purchase_record(args):
    """
    普通用户消费记录
    :param args: 元组里面数据有:账户ID, 消费金额, 消费时间
    :return:
    """
    conn_params = settings.DATABASE
    db_path = "%s/%s/%s" % (conn_params['path'], conn_params['record'], args["id"])
    print(db_path)
    str_args = json.dumps(args)
    with open(db_path, "a+", encoding="utf-8") as wf:
        wf.writelines(str_args+'\n')


def read_purchase_record(args):
    """
    普通用户查询消费记录
    :param args:
    :return:
    """
    conn_params = settings.DATABASE
    db_path = "%s/%s/%s" % (conn_params['path'], conn_params['record'], args)
    print(db_path)
    with open(db_path, "r", encoding="utf-8") as rf:
        for usr_rec in rf:
            rec_dict = eval(usr_rec)
            print(rec_dict)
