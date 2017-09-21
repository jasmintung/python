# 因为增加,删除,修改模块都要经过查询模块
import os
import sys
import json
from conf import settings
from core import employ
file_path = "%s/%s" % (settings.DATABASE["path"], settings.DATABASE["name"])
# from functools import wraps
# def process(arg): # arg目前作为用户选择功能区分
#     if arg != 0:
#         def deco(func):
#             @wraps(func)
#             def wrapper(*args, **kwargs):
#                 print("deco it")
#                 # 这里进行查询处理
#                 employ_info = {}
#                 tmpstr = args[0].__str__()
#                 print(type(tmpstr))
#                 employ_info = eval(tmpstr)
#                 print("your id is ", employ_info["starffId"])
#                 print("your name is ", employ_info["name"])
#                 # print("your id is ", args[0][0])
#                 # print("your name is", args[0][1])
#                 # ...WW
#                 taskid = 1
#                 funcers = func(taskid, *args, **kwargs)
#                 return funcers
#             return wrapper
#     else:
#         def deco(func):
#             return func
#     return deco


def process(index=3, *args, **kwargs):
    if os.path.getsize(file_path) <= 0:
        if index == 1:  # 增加员工
            print("indid add is ok don't need check")
            return True
        else:
            print("db is empty!!!")
            return False
    return search_process(index, args)


def search_process(index, args):  # 不能再写*args否则形参会成为元组的元组((....))
    result = False
    if index == 3:

        instructions = """
            1: 搜索大于输入的id的员工信息
            2: 搜索小于输入的id的员工信息
            3: 搜索大于输入的年龄的员工信息
            4: 搜索小于输入的年龄的员工信息
            5: 搜索输入的部门的员工信息
            6: 搜索输入的姓名对应的员工信息
            7: 搜索符合日期的员工信息
        """
        print(instructions)
        choice = input("input your select type: ")
        if choice.isdigit() and int(choice) < 8:
            employ.db_to_usr(choice)
        else:
            print("无效操作")
            return result
    else:
        with open(file_path, "r", encoding="utf-8") as fp:
            if index == 1:  # 增加
                employ_info = {}
                tmpstr = args[0].__str__()  # 因为元组的格式是({"key1": "1312"},)
                employ_info = eval(tmpstr)
                result = True
                for epinfo in fp:
                    # print(epinfo.strip('\n'))  # 打印并过滤每一行末尾的\n
                    tmp_dict = eval(epinfo)
                    # print(type(tmp_dict))
                    if tmp_dict.get("starffId") == employ_info.get("starffId") \
                        or tmp_dict.get("name") == employ_info.get("name"):
                        result = False
            elif index == 2:  # 删除
                attr = args[0]
                val = args[1]
                for epinfo in fp:
                    tmp_dict = eval(epinfo)
                    if attr == "starffId":
                        if tmp_dict.get("starffId") == int(val):
                            return True
                    elif attr == "name":
                        if tmp_dict.get("name") == val:
                            return True
                    elif attr == "age":
                        if tmp_dict.get("age") == int(val):
                            return True
                    elif attr == "phone":
                        if tmp_dict.get("phone") == int(val):
                            return True
                    elif attr == "dept":
                        if tmp_dict.get("dept") == val:
                            return True
                    else:
                        print("!!!not support")
            elif index == 4:  # 修改
                pass
    return result
