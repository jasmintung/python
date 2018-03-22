#!usr/bin/env python
# -*- coding:utf-8 -*-
# auther:Tony Cheung
# 描述：window 环境下测试通过.
from core import UserControl
host = 'localhost'
port = 9986


def main():
    notice = """
    ******欢迎使用FTP工具******
    1、上传文件
    2、下载文件
    0、退出
    """
    while True:
        print(notice)
        choice = input("请选择:")
        user_instance = UserControl.UserControl(host, port)
        if choice == '1':
            user_instance.upload()
        elif choice == '2':
            user_instance.download()
        elif choice == '0':
            exit()
        else:
            print("输入有误")
