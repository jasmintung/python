# -*- coding:utf-8 -*-
__author__ = 'zhangtong'

import os,sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
sys.path.append(BASE_DIR)

if __name__ == '__main__':
    """堡垒机管理程序入口地址"""
    from modules.actions import excute_from_command_line
    excute_from_command_line(sys.argv)

