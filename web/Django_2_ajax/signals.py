from django.db.models.signals import pre_save
from logs import logger
import django.dispatch
import os, sys


checkdir = os.path.dirname(os.path.abspath(__file__)) + '/logs/log'
if os.path.exists(checkdir) is False:
    os.makedirs(checkdir)

handle_save_log = None  # 保存操作记录
handle_unexcept_log = None  # 异常情况记录


def rc_presave_log(sender, **kwargs):
    print("record log...")
    print(kwargs)
    global handle_save_log
    if not handle_save_log:
        handle_save_log = logger.logger("db_save_log")
    handle_save_log.info(kwargs)


pre_save.connect(rc_presave_log)


def rc_unexpect_log(sender, **kwargs):
    print("exception record log...")
    global handle_unexcept_log
    if not handle_unexcept_log:
        handle_unexcept_log = logger.logger("err_log")
    handle_unexcept_log.error(kwargs)


handel_err_s = django.dispatch.Signal(providing_args=["err_type", "content"])  # 自定义异常信号
handel_err_s.connect(rc_unexpect_log)  # 注册
