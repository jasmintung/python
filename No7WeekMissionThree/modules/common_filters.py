# -*- coding=utf-8-*-
__author__ = 'zhangtong'

from modules import models
from modules.db_conn import engine, session
from modules.utils import print_err


def bind_hosts_filter(vals):
    """
    在主机绑定表里查询
    :param vals:
    :return:
    """
    print("***>", vals.get('bind_hosts'))
    bind_hosts = session.query(models.BindHost).filter(models.Host.hostname.in_(vals.get('bind_hosts'))).all()
    if not bind_hosts:
        print_err("None of [%s] exist in bind_host table." % vals.get('bind_hosts'), quit=True)
    else:
        return bind_hosts


def user_profiles_filter(vals):
    """
    在用户表里查询
    :param vals:
    :return:
    """
    user_profiles = session.query(models.UserProfile).filter(models.UserProfile.username.in_(vals.get('user_profiles'))
                                                             ).all()
    if not user_profiles:
        print_err("None of [%s] exist in user_profile table." % vals.get('user_profiles'), quit=True)
    else:
        return user_profiles
