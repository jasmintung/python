from core import db_handler


def process():
    print("modify func")
    notice = "UPDATE Person SET dept= \"Market\" WHERE dept = \"IT\""
    print("请输入SQL 更新 语句比如 %s:" % notice)
    sql_update = input()
    if sql_update.startswith("UPDATE") and sql_update.find("WHERE"):
        value_level_1 = sql_update.split("WHERE")
        dst_dept = value_level_1[0].split("=")[1].lstrip(" ")
        source_dept = value_level_1[1].split("=")[1].strip(" ")
        db_api = db_handler.db_handler()
        db_api("UPDATE Person SET dept=%s WHERE dept =%s" % (dst_dept, source_dept))  # 如果需要增加其它类型的修改支持,在这个函数里面添加代码即可
    else:
        print("输入错误")