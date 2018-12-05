#!usr/bin/env python
# -*- coding:utf-8 -*-
# auther:Tony Cheung
# 描述：window 环境下测试通过.

import sys
import threading
from core import UserControl
from core.view import LoginDialog
from core.view import MissionUI
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
host = 'localhost'
port = 9986


def main():
    notice = """
    ******欢迎使用FTP工具******
    1、上传文件
    2、下载文件
    0、退出
    """
    app = QApplication(sys.argv)
    print("app:", app)
    instance = LoginDialog.init(app)
    # print("main thread:", threading.current_thread())
    if instance.exec_() == QtWidgets.QDialog.Accepted:  # 判断登陆界面是否退出了
        MissionUI.initMissionUI(app)  # 初始化主界面
        # sys.exit(app.exec_())
    # instance.login_result_signal.connect(login_result)
    sys.exit(app.exec_())

    # while True:
    #     print(notice)
    #     choice = input("请选择:")
    #     user_instance = UserControl.UserControl(host, port)
    #     if choice == '1':
    #         user_instance.upload()
    #     elif choice == '2':
    #         user_instance.download()
    #     elif choice == '0':
    #         exit()
    #     else:
    #         print("输入有误")


def login_result(result):
    if result == "OK":
        print("ok")
        # QtCore.QCoreApplication.quit()
        MissionUI.initMissionUI()
    else:
        print("not pass")
