# -*- coding:utf-8 -*-
__author__ = 'zhangtong'

import os
import sys
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)

from conf import database_config
# 数据库初始化配置
DB_CONN = "mysql+pymysql://%s:%s@localhost:%d/%s?charset=utf8" % (database_config.USER_NAME,
                                                                   database_config.PASSWORD,
                                                                   database_config.PORT,
                                                                   database_config.DATABASE_NAME)
print(DB_CONN)
# YML_DIR = BASE_DIR + os.sep + "share" + os.sep + "yml_source" + os.sep
# YML文件存储目录
YML_DIR = os.sep.join([BASE_DIR, "share", "yml_source"])
print(YML_DIR)

# 打印等级
LOG_LEVEL = logging.INFO
LOG_DIR = BASE_DIR + os.sep + "log"
