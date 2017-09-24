from core import search_ep
from core import db_handler

import time
import re
strip = re.compile(r'[^(].*[^)]')  # 去掉括号规则
bracket = re.compile(r'\([^()]+\)')  # 获取values
employ_info = {
    "starffId": None,
    "name": None,
    "age": None,
    "phone": None,
    "dept": None,
    "enroll date": None
}


def process():

    notice = """INSERT INTO Persons VALUES ('1', 'zhangtong', '29', '15999000001', 'soft')"""
    print("请输入SQL 插入 语句比如: %s" % notice)
    sql_insert = input();
    if sql_insert.startswith("INSERT") and sql_insert.find("VALUES"):
        key = sql_insert.split("VALUES")[0]
        print(bracket.search(sql_insert).group())
        input_employ_info = strip.search(bracket.search(sql_insert).group()).group()
        tuple_employ_info = tuple(eval(input_employ_info))
        id = int(tuple_employ_info[0])
        name = tuple_employ_info[1]
        age = int(tuple_employ_info[2])
        phone = tuple_employ_info[3]
        dept = tuple_employ_info[4]

        employ_info["starffId"] = id
        employ_info["name"] = name
        employ_info["age"] = age
        employ_info["phone"] = phone
        employ_info["dept"] = dept
        employ_info["enroll date"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 将本地时间戳 struct_time格式转成指定的字符串格式
        if search_ep.process(1, employ_info) is True:
            add_process(key, employ_info)
        else:
            print("已经有这个人了!")
    else:
        print("输入不正确!")


def add_process(key, args):
    db_api = db_handler.db_handler()
    db_api("%sVALUES = %s" %(key, args))




