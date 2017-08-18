# 因为增加,删除,修改模块都要经过查询模块,所以本模块应该做成装饰器
from functools import wraps


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
    if index != 3: # 针对增删改
        print("gogogo")
    else:                                       # 针对自身查找
        print("yeyeyey")

