# __author__ :"zhangtong"

"""
handler all the logging works
"""
import logging
import os


def logger(log_type):

    # create logger
    logger = logging.getLogger(log_type)
    logger.setLevel(logging.INFO)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # create file handler and set level to warning
    log_file = "%s/log/%s" % (os.path.dirname(os.path.abspath(__file__)), log_type)
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.INFO)

    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # add formatter to ch and fh
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add ch and fh to logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger