from core import db_handler
from core import search_ep


def process():
    """
    目前支持根据姓名,年龄,电话,部门删除,后续要新增直接在这个函数里面处理即可
    :return:
    """
    print("delete func")
    notice = """
    DELETE FROM Person WHERE starffId = 1,
    DELETE FROM Person WHERE name = 'lisi',
    DELETE FROM Person WHERE age = 18,
    DELETE FROM Person WHERE phone = '0755110',
    DELETE FROM Person WHERE dept = 'soft',
    """
    print("请输入SQL 删除 语句比如 %s:" % notice)

    sql_delete = input()
    if sql_delete.startswith("DELETE") and sql_delete.find("WHERE"):
        key = sql_delete.split("WHERE")[0].rstrip(" ")
        value = sql_delete.split("WHERE")[1].strip(" ")
        attr_val = value.split("=")
        attr = attr_val[0].rstrip(" ")
        val = attr_val[1].lstrip(" ").strip("'")
        if search_ep.process(2, attr, val) is True:
            return delete_process(key, attr, val)
        else:
            print("没有这个人!")
    else:
        print("输入错误")

def delete_process(key, *args):
    db_api = db_handler.db_handler()
    db_api("%s WHERE %s = %s" % (key, args[0], args[1]))