import time
from core import db_handler
from conf import settings


def idA():
    print("idA")


def idB():
    print("idB")


def ageA():
    print("ageA")


def ageB():
    print("ageB")


def dept_str():
    print("dept_str")


def name_str():
    print("name_str")


def enroo_date_str():
    print("enroo_date_str")


select_func = {"1": idA, "2": idB, "3": ageA, "4": ageB, "5": dept_str, "6": name_str, "7": enroo_date_str}


def db_to_usr(args):
    db_api = db_handler.db_handler()
    select_func[args]()
    # db_api("select * from employs where starffId > %s" % args)
    # db_api("select * from employs where starffId < %s" % args)
    # db_api("select * from employs where age > %s" % args)
    # db_api("select * from employs where age < %s" % args)
    # db_api("select * from employs where dept = %s" % args)
    # db_api("select * from employs where name like %s" % args)
    # db_api("select * from employs where enroll date like %s" % args)


def usr_to_db(args):
    print("modify or add or delete!")