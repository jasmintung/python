# -*- coding:utf-8 -*-
__author__ = 'zhangtong'

import os

from conf import database_config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_CONN = "mysql+pymysql://%s:%s@localhost:%d/%s?charset=utf-8" % (database_config.USER_NAME,
                                                                   database_config.PASSWORD,
                                                                   database_config.PORT,
                                                                   database_config.DATABASE_NAME)
