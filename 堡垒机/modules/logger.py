# -*-coding:utf-8-*-
__author__ = "zhangtong"
import logging

from conf import settings


def logger_manager(user_name):
    # create logger根据登陆用户名来创建文件
    logger = logging.getLogger(user_name)
    logger.setLevel(settings.LOG_LEVEL)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(settings.LOG_LEVEL)

    # create file handler and set level by settings
    log_file = "%s/%s" % (settings.LOG_DIR, user_name)
    fh = logging.FileHandler(log_file)
    fh.setLevel(settings.LOG_LEVEL)

    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # add formatter to ch and fh
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add ch and fh to logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger
