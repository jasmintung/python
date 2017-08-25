from core import db_handler


def process():
    print("modify func")
    db_api = db_handler.db_handler()
    sourc_dept = input("input which dept you want to modify")
    dst_dept = input("input the dept you want to set")
    db_api("update staff_table SET dept=%s where dept =%s" % (dst_dept, sourc_dept)) # 如果需要增加其它类型的修改支持,在这个函数里面添加代码即可