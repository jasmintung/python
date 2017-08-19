# 因为增加,删除,修改模块都要经过查询模块
import os
import sys
import json
from conf import settings


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
    if os.path.getsize(settings.BASE_DB) <= 0:
        if index == 1:  # 增加员工
            print("indid add is ok don't need check")
            return True
        else:
            print("db is empty!!!")
            return False
    return search_process(index, args)


def search_process(index, args): #不能在写*args否则形参会成为元组的元组((....))
    result = False
    employ_info = {}
    print(args)
    tmpstr = args[0].__str__()
    print(type(tmpstr))
    employ_info = eval(tmpstr)
    print(type(employ_info))
    with open(settings.BASE_DB, "r" ,encoding="utf-8") as fp:
        for epinfo in fp:
            print(epinfo.strip('\n')) #打印并过滤每一行末尾的\n
            tmp_dict = eval(epinfo)
            print(type(tmp_dict))
            if tmp_dict.get("starffId") == employ_info.get("starffId") \
                or tmp_dict.get("name") == employ_info.get("name"):
                print("已存在,不能增加!!")
                result = False
    return result
