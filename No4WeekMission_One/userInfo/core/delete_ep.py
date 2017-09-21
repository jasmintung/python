from core import db_handler
from core import search_ep


def process():
    """
    目前支持根据姓名,年龄,电话,部门删除,后续要新增直接在这个函数里面处理即可
    :return:
    """
    print("delete func")
    notic = """
    输入数字 1 根据 ID 删除
    输入数字 2 根据 姓名 删除
    输入数字 3 根据 年龄 删除
    输入数字 4 根据 电话 删除
    输入数字 5 根据 部门 删除
    """
    print(notic)
    your_choice = int(input("your choic is no."))
    attr = ""
    val = ""

    if your_choice == 1:
        attr = "starffId"
        val = int(input("输入Id: "))
    elif your_choice == 2:
        attr = "name"
        val = input("输入姓名: ")
    elif your_choice == 3:
        attr = "age"
        val = int(input("输入年龄: "))
    elif your_choice == 4:
        attr = "phone"
        val = int(input("输入电话号码: "))
    elif your_choice == 5:
        attr = "dept"
        val = input("输入部门: ")
    else:
        print("not support")
        return False
    if search_ep.process(2, attr, val) is True:
        return delete_process(attr, val)
    else:
        print("没有这个人!")


def delete_process(*args):
    db_api = db_handler.db_handler()
    db_api("delete * from staff_table where %s = %s" % (args[0], args[1]))