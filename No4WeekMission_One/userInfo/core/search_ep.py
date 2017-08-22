# 因为增加,删除,修改模块都要经过查询模块
import os
import sys
import json
from conf import settings
from core import employ
file_path = "%s/%s" %(settings.DATABASE["path"], settings.DATABASE["name"])
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


def search_process(index, args): #不能再写*args否则形参会成为元组的元组((....))
    result = False
    if index == 3:

        instructions = """
            1:you can select the employ info by employ id which > your input value
            2:you can select the employ info by employ id which < your input value
            3:you can select the employ info by employ age which > your input value
            4:you can select the employ info by employ age which < your input value
            5:you can select the employ info by company dept which your input value is equal in the dept
            6:you can select the employ info by employ name which your input value is exist in the name
            7:you can select the employ info by employ date which your input value is exist in the date
        """
        print(instructions)
        choice = input("input your select type: ")
        if choice.isdigit() and int(choice) < 8:
            employ.db_to_usr(choice)
    with open(file_path, "r", encoding="utf-8") as fp:
        if index == 1: # 增加
            employ_info = {}
            tmpstr = args[0].__str__() # 因为元组的格式是({"key1": "1312"},)
            employ_info = eval(tmpstr)
            result = True
            for epinfo in fp:
                print(epinfo.strip('\n')) #打印并过滤每一行末尾的\n
                tmp_dict = eval(epinfo)
                print(type(tmp_dict))
                if tmp_dict.get("starffId") == employ_info.get("starffId") \
                    or tmp_dict.get("name") == employ_info.get("name"):
                    print("已存在,不能增加!!")
                    result = False
        elif index == 2: # 删除
            pass
    return result
