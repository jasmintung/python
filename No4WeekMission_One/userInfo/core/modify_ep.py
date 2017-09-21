from core import db_handler


def process():
    print("modify func")
    db_api = db_handler.db_handler()
    sourc_dept = input("输入您想修改的部门名称")
    dst_dept = input("输入您想设置的部门名称")
    db_api("update staff_table SET dept=%s where dept =%s" % (dst_dept, sourc_dept))  # 如果需要增加其它类型的修改支持,在这个函数里面添加代码即可
