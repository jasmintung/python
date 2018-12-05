from core.student import StudentModule
from core.teacher import TeacherModule
from core.admin import AdminModule


def run():
    # 程序主入口

    while True:
        instance_type = None
        print("***欢迎使用选课系统***")
        charactor = int(input("请选择登陆角色: 1: 学员 2: 讲师 8: 管理员 0: 退出"))
        if charactor == 1:
            instance_type = StudentModule()
        elif charactor == 2:
            instance_type = TeacherModule(None)
        elif charactor == 8:
            instance_type = AdminModule()
        elif charactor == 0:
            break
        else:
            print("选择不正确哦!")
            continue
        role_select(instance_type)
        login_result = instance_type.login_result()
        if login_result[0] == 2:  # 进入账户注册环节, 仅适用与学员 讲师
            role_register(instance_type)
        elif login_result[0] == 0:  # 将当前登陆的用户名传入用户操作接口
            role_operation(instance_type, login_result[1])
        else:
            pass


def role_select(obj):
    obj.auth()


def role_register(obj):
    obj.register()


def role_operation(obj, role_name):
    obj.control_operation(role_name)
