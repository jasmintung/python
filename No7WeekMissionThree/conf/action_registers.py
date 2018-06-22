# -*- coding:utf-8 -*-
__author__ = 'zhangtong'

from modules import views

actions = {
    'start_session': views.start_session,
    'stop': views.stop_server,
    'syncdb': views.syncdb,
    'create_users': views.create_users,
    'create_groups': views.create_groups,
    'create_hosts': views.create_hosts,
    'create_bindhosts': views.create_bindhosts,
    'create_remoteusers': views.create_remoteusers,
}