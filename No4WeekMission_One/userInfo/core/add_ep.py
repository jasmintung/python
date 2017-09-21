from core import search_ep
from core import db_handler

import time

employ_info = {
    "starffId": None,
    "name": None,
    "age": None,
    "phone": None,
    "dept": None,
    "enroll date": None
}


def process():
    print("add func")
    id = int(input("请输入员工编号(1~9999999)"))
    name = input("清输入员工姓名: ")
    age = int(input("请输入员工年龄: "))
    phone = input("请输入员工电话: ")
    dept = input("请输入员工部门: ")
    employ_info["starffId"] = id
    employ_info["name"] = name
    employ_info["age"] = age
    employ_info["phone"] = phone
    employ_info["dept"] = dept
    employ_info["enroll date"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 将本地时间戳 struct_time格式转成指定的字符串格式
    if search_ep.process(1, employ_info) is True:
        add_process(employ_info)
    else:
        print("已经有这个人了!")


def add_process(args):
    db_api = db_handler.db_handler()
    db_api("insert into staff_table values = %s" % args)




