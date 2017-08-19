from core import auth
from core import add_ep
from core import delete_ep
from core import modify_ep
from core import search_ep

func_dict = {"1": add_ep, "2": delete_ep, "3": search_ep, "4": modify_ep}


def fun_entry(arg):
    """
    根据用户输入调用对应的功能
    :param arg: 1,2,3,4
    :return: 处理结果
    """
    # print(func_dict[str(arg)])
    func_dict[str(arg)].process()


def run():
    auth.auth_process()
    while True:
        main_menu = """
        \t\t******请选择******
        1: 增加员工信息\t2: 删除员工信息
        3: 查找员工信息\t4: 修改员工信息
        5: 退出
        """
        print(main_menu)
        choice = int(input(">>").strip())
        print(choice)
        if choice == 5:
            print("exit")
            break
        else:
            fun_entry(choice)




# from functools import wraps
#
#
# def task_logging(taskname):
#     def func_wrapper(func):
#         @wraps(func)
#         def return_wrapper(*args, **wkargs):
#             # 函数通过装饰起参数给装饰器传送参数
#             print('before task',taskname)
#             # 装饰器传变量给函数
#             taskid = 1
#             summer, funcres = func(taskid, *args, **wkargs)
#             print('after task', taskid, summer)
#             return funcres
#         return return_wrapper
#     return func_wrapper
#
#
# @task_logging("test")
# def testd(taskid):
#     print("testd runing",taskid)
#     return "task summer success eg", []
#
# testd()