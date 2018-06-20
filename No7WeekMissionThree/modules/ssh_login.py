# -*- coding:utf-8-*-
__author__ = 'zhangtong'
# 这里面是对paramiko 中ssh_login.py源码的基础上进行修改

import base64
import getpass
import os
import sys
import socket
import traceback
from paramiko.py3compat import input
from modules import models
import datetime
import paramiko

try:
    import interactive
except ImportError:
    from . import interactive


def ssh_login(user_obj, bind_host_obj, mysql_engine, log_recording):
    #  now, connect and use paramiko Client to negotiate SSH2 across the connection
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())
        print("*** Connecting...")
        client.connect(bind_host_obj.host.ip_addr,
                       bind_host_obj.host.port,
                       bind_host_obj.remoteuser.username,
                       bind_host_obj.remoteuser.password,
                       timeout=30)
        cmd_caches = []
        chan = client.invoke_shell()
        print(repr(client.get_transport()))
        print("** Here we go!\n")
        cmd_caches.append(models.AuditLog(user_id=user_obj.id,
                                          bind_host_id=bind_host_obj.id,
                                          action_type='login',
                                          data=datetime.datetime.now()
                                          ))
        log_recording(user_obj, bind_host_obj, cmd_caches)
        interactive.interactive_shell(chan, user_obj, bind_host_obj, cmd_caches, log_recording)
        chan.close()
        client.close()

    except Exception as e:
        print("*** Caught exception: %s: %s" % (e.__class__, e))
        traceback.print_exc()
        try:
            pass
        except:
            pass
        sys.exit(1)
