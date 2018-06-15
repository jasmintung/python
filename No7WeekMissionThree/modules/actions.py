# -*- coding:utf-8 -*-
__author__ = 'zhangtong'

from conf import settings
from conf import action_registers


def help_msg():
    """帮助提示"""
    print("\033[31;1mAvailable commmands:\033[0m")
    for key in action_registers.actions:
        print("\t", key)


def excute_from_command_line(argvs):
    if len(argvs) < 2:
        help_msg()
        exit()
    if argvs[1] not in action_registers.actions:
        pass
    action_registers.actions[argvs[1]](argvs[1:])
