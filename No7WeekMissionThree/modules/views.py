import sys
import os
from conf import settings
from modules import models
from modules.db_conn import engine, session
from modules.utils import print_err, yaml_parse
from modules import ssh_login
from modules import common_filters

logger_instance = None


def auth():
    count = 0
    while count < 3:
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
            from modules import logger
            global logger_instance
            if logger_instance is None:
                pass
            else:
                logger_instance = logger.logger_manager(user_obj.username)
            return user_obj
        else:
            print("wrong username or password, you have %s more chances." % (3 - count - 1))
            count += 1
    else:
        print_err("too many attempts.")


def welcome_msg(user):
    WELCOME_MSG = """\033[32;1m
    -------- Welcome [%s] login BaoLei Machine --------\033[0m""" % user.username
    print(WELCOME_MSG)


def log_recording(user_obj, bind_host_obj, logs):
    """
    用户操作记录日志
    :param user_obj: 操作的用户对象
    :param bind_host_obj: 绑定主机对象
    :param logs: 用户输入的指令的存储列表
    :return:
    """
    if logger_instance is None:
        print_err("\033[31;1m###log manager not init!\033[0m")
    else:
        logger_instance.info("operation host name is:%s ip is: %s\nActions are:%s" %
                             (bind_host_obj.host.hostname, bind_host_obj.host.ip_addr,
                              ",".join('%s' % cmd for cmd in logs)))


def start_session(args):
    print(args)
    user = auth()
    if user:
        welcome_msg(user)
        print(user.bind_hosts)  # 绑定表
        print("user.Groups:", user.Groups)  # 用户所在的组
        exit_flag = False
        while not exit_flag:
            # 获取组表信息, 打印组表信息
            if user.bind_hosts:
                print("\033[32;1mz.\tungroupped hosts (%s)\033[0m" % len(user.bind_hosts))
            for index, group in enumerate(user.Groups):
                print("\033[32;1m%s.\t%s (%s)\033[0m" % (index, group.name, len(group.bind_hosts)))

            choice = input("[%s]:" % user.username).strip()
            if len(choice) == 0:
                continue
            if choice == 'z':
                pass
            elif choice.isdigit():
                choice = int(choice)  # 选择分组
                if choice < len(user.Groups):
                    print("------ Group: %s ------" % user.Groups[choice].name)
                    for index, bind_host in enumerate(user.Groups[choice].bind_hosts):
                        print("   %s.\t%s@%s(%s)" % (index,
                                                     bind_host.remoteuser.username,
                                                     bind_host.host.hostname,
                                                     bind_host.host.ip_addr))
                    print("---------- END ----------")

                    # 主机选择(根据ID)
                    while not exit_flag:
                        user_option = input("[(b)back, (q)quit, select host to login:]").strip()
                        if len(user_option) == 0:
                            continue
                        if user_option == 'b':
                            break
                        if user_option == 'q':
                            exit_flag = True
                        if user_option.isdigit():
                            user_option = int(user_option)
                            if user_option < len(user.Groups[choice].bind_hosts):
                                print('host:', user.Groups[choice].bind_hosts[user_option])
                                print('audit log:', user.Groups[choice].bind_hosts[user_option].audit_logs)
                                #  开始发起paramiko ssh远程登录主机
                                ssh_login.ssh_login(user,
                                                    user.Groups[choice].bind_hosts[user_option],
                                                    session,
                                                    log_recording)
                            else:
                                print("no this option...")


def stop_server():
    pass


def create_users(argvs):
    """
    创建用户信息，从文件读取写入数据库，事先要配置好文件
    :return:
    """
    if '-f' in argvs:
        user_file = argvs[argvs.index("-f") + 1]
    else:
        print_err("invalid usage, should be\ncreateusers -f <the new users file>", quit=True)
    print(settings.YML_DIR + os.sep + user_file)
    source = yaml_parse(settings.YML_DIR + os.sep + user_file)
    if source:
        for key, val in source.items():
            print(key, val)
            obj = models.UserProfile(username=key, password=val.get('password'))
            if val.get('groups'):
                # 先查看用户是否在分组中
                groups = session.query(models.Group).fileter(models.Group.name.in_(val.get('groups'))).all()
                if not groups:
                    print_err("None of [%s] exist in group table." % val.get('groups'), quit=True)
                obj.groups = groups
            if val.get('bind_hosts'):
                # 查看用户是否在绑定表里
                bind_hosts = common_filters.bind_hosts_filter(val)
                obj.bind_hosts = bind_hosts

            session.add(obj)
        session.commit()


def create_groups(argvs):
    """
    创建组信息，从文件读取写入数据库，事先要配置好文件
    :return:
    """
    if '-f' in argvs:
        group_file = argvs[argvs.index("-f") + 1]
    else:
        print_err("invalid usage, should be\ncreategroups -f <the new groups file>", quit=True)
    print(settings.YML_DIR + os.sep + group_file)
    source = yaml_parse(settings.YML_DIR + os.sep + group_file)
    if source:
        for key, val in source.items():
            print(key, val)
            obj = models.Groups(name=key)
            if val.get('bind_hosts'):
                bind_hosts = common_filters.bind_hosts_filter(val)
                obj.bind_hosts = bind_hosts

            if val.get('user_profiles'):
                user_profiles = common_filters.user_profiles_filter(val)
                obj.user_profiles = user_profiles
            session.add(obj)
        session.commit()


def create_hosts(argvs):
    """
    创建主机信息,从文件读取写入数据库,事先要配置好文件
    :return:
    """
    if '-f' in argvs:
        hosts_file = argvs[argvs.index("-f") + 1]
    else:
        print_err("invalid usage, should be:\ncreate_hosts -f < the new hosts file >", quit=True)
    print(settings.YML_DIR + os.sep + hosts_file)
    source = yaml_parse(settings.YML_DIR + os.sep + hosts_file)
    if source:
        for key, val in source.items():
            print(key, val)
            obj = models.Host(hostname=key, ip_addr=val.get('ip_addr'), port=val.get('port') or 22)
            session.add(obj)
        session.commit()


def create_bindhosts(argvs):
    """
    创建绑定关系表
    :return:
    """
    if '-f' in argvs:
        bindhosts_file = argvs[argvs.index("-f") + 1]
    else:
        print_err("invalid usage, should be:\ncreate_bindhosts -f <the new bindhosts file>", quit=True)
    print(settings.YML_DIR + os.sep + bindhosts_file)
    source = yaml_parse(settings.YML_DIR + os.sep + bindhosts_file)
    if source:
        for key, val in source.items():
            host_obj = session.query(models.Host).filter(models.Host.hostname == val.get('hostname')).first()
            assert host_obj
            for item in val['remote_users']:
                assert item.get('auth_type')
                if item.get('auth_type') == 'ssh-passwd':
                    remoteuser_obj = session.query(models.RemoteUser).filter(
                        models.RemoteUser.username == item.get('username'),
                        models.RemoteUser.password == item.get('password')
                    ).first()
                else:
                    remoteuser_obj = session.query(models.RemoteUser).filter(
                        models.RemoteUser.username == item.get('username'),
                        models.RemoteUser.auth_type == item.get('auth_type')
                    )
                if remoteuser_obj is None:
                    print_err("RemoteUser obj %s dose not exist." % item, quit=True)
                else:
                    bindhost_obj = models.BindHost(host_id=host_obj.id, remote_user_id=remoteuser_obj.id)
                    session.add(bindhost_obj)
                    if source[key].get('groups'):
                        group_objs = session.query(models.Groups).filter(models.Groups.name.in_(source[key].get('groups'))).all()
                        assert group_objs
                        print('groups:', group_objs)
                        bindhost_obj.groups = group_objs
                    if source[key].get('user_profiles'):
                        userprofile_objs = session.query(models.UserProfile).filter(models.UserProfile.username.in_(
                            source[key].get('user_profiles')
                        )).all()
                        assert userprofile_objs
                        bindhost_obj.user_profiles = userprofile_objs
        session.commit()


def create_remoteusers(argvs):
    """
    创建远程登录账户信息,从文件读取写入数据库,事先要配置好文件
    :return:
    """
    if '-f' in argvs:
        remoteusers_file = argvs[argvs.index("-f") + 1]
        print("remoteusers_file:", remoteusers_file)
    else:
        print_err("invalid usage, should be:\ncreate_remoteusers -f <the new remoteusers file>", quit=True)
    print(settings.YML_DIR + os.sep + remoteusers_file)
    source = yaml_parse(settings.YML_DIR + os.sep + remoteusers_file)
    if source:
        for key, val in source.items():
            print(key, val)
            obj = models.RemoteUser(username=val.get('username'),
                                    auth_type=val.get('auth_type'),
                                    password=val.get('password'))
            session.add(obj)
        session.commit()


def syncdb(argvs):
    print("Syncing DB...")
    models.Base.metadata.create_all(engine)  # 创建数据库
