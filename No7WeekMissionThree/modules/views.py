import sys
from modules import models
from modules.db_conn import engine, session
from modules.utils import print_err, yaml_parse


def auth():
    count = 0
    while count > 3:
        username = input("\033[32;1mUsername:\033[0m").strip()
        if len(username) == 0:
            continue
        password = input("\033[32;1mPassword:\033[0m").strip()
        if len(password) == 0:
            continue
        # 去堡垒机数据库查看用户是否存在
        user_obj = session.query(models.UserProfile).filter(models.UserProfile.username == username,
                                                            models.UserProfile.password == password).first()
        if user_obj:
            return user_obj
        else:
            print("wrong username or password, you have %s more chances." % (3-count-1))
            count += 1
    else:
        print_err("too many attempts.")


def welcome_msg(user):
    WELCOME_MSG = """\033[32;1m
    -------- Welcome [%s] login BaoLei Machine --------\033[0m""" % user.username
    print(WELCOME_MSG)


def start_session(args):
    print(args)
    user = auth(
    if user:
        welcome_msg(user)
        print(user.bind_hosts)  # 绑定表
        print(user.groups)  # 用户所在的组
        exit_flag = False
        while not exit_flag:
            # 获取组表信息, 打印组表信息
            if user.bind_hosts:
                print("\033[32;1mz.\tungroupped hosts (%s)\033[0m" % len(user.bind_hosts))
            for index, group in enumerate(user.groups):
                print("\033[32;1m%s.\t%s (%s)\033[0m" % (index, group.name, len(group.bind_hosts)))

            choice = input("[%s]:" % user.username).strip()
            if len(choice) == 0:
                continue
            if choice == 'z':
                pass
            elif choice.isdigit():
                choice = int(choice) # 选择分组
                if choice < len(user.groups):
                    print("------ Group: %s ------" % user.groups[choice].name)
                    for index, bind_host in enumerate(user.groups[choice].bind_hosts)
                        
def stop_server():
    pass


def create_users():
    pass


def create_groups():
    pass


def create_hosts():
    pass


def create_bindhosts():
    pass


def create_remoteusers():
    pass


def syncdb():
    pass
