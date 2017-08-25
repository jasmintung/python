import time
from core import db_handler
from conf import settings


def idA(args):
    print("idA")
    id = int(input("\ninput the employ id(1~99999)"))
    args("select * from employs where starffId > %s" % id)


def idB(args):
    print("idB")
    id = int(input("input the employ id(1~99999"))
    args("select *from employes where starffId < %s" % id)


def ageA(args):
    print("ageA")
    age = int(input("input the employ age(16~200"))
    args("select *from employes where age > %s" % age)


def ageB(args):
    print("ageB")
    age = int(input("input the employ age(16~200"))
    args("select *from employes where age < %s" % age)


def dept_str(args):
    print("dept_str")
    dept = input("input the employ dept")
    args("select *from employes where dept = %s" % dept)


def name_str(args):
    print("name_str")
    name = input("input the xxnamexx")
    args("select *from employes where name like %s" % name)


def enroo_date_str(args):
    print("enroo_date_str")
    e_date = input("input the date type as xxxx-xx-xx")
    args("select * from employs where enroll date like %s" % e_date)

select_func = {"1": idA, "2": idB, "3": ageA, "4": ageB, "5": dept_str, "6": name_str, "7": enroo_date_str}


def db_to_usr(args):
    db_api = db_handler.db_handler()
    select_func[args](db_api)


def usr_to_db(args):
    print("modify or add or delete!")