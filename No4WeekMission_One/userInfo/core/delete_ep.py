from core import db_handler
from core import search_ep


def process():
    """
    目前只支持根据姓名删除,后续要新增直接在这个函数里面处理即可
    :return:
    """
    print("delete func")
    notic = """
    choice 1 you can delete by id
    choice 2 you can delete by name
    choice 3 you can delete by age
    choice 4 you can delete by phone
    choice 5 you can delete by dept
    """
    print(notic)
    your_choice = int(input("your choic is no."))
    attr = ""
    val = ""
    if your_choice.isdigit():
        if your_choice == 1:
            attr = "starffId"
            val = int(input("input employ id: "))
        elif your_choice == 2:
            attr = "name"
            val = input("input employ name: ")
        elif your_choice == 3:
            attr = "age"
            val = int(input("input employ age: "))
        elif your_choice == 4:
            attr = "phone"
            val = int(input("input employ phone: "))
        elif your_choice == 5:
            attr = "dept"
            val = input("input employ dept: ")
        else:
            print("not support")
            return False
        if search_ep.process(2, attr, val) is True:
            return delete_process(attr, val)


def delete_process(*args):
    db_api = db_handler.db_handler()
    db_api("delete * from staff_table where %s = %s" % (args[0], args[1]))
