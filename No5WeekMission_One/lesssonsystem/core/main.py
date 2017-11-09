from core.student import StudentModule
from core.teacher import TeacherModule
from core.admin import AdminModule


def run():
    # 程序主入口
    while True:
        print("***欢迎使用选课系统***")
        charactor = int(input("请选择登陆角色: 1: 学员 2: 讲师 8: 管理员"))
        instance_type = None
        if charactor == 1:
            instance_type = StudentModule()
        elif charactor == 2:
            instance_type = TeacherModule()
        elif charactor == 8:
            instance_type = AdminModule()
        else:
            print("选择不正确哦!")
            continue
        print(instance_type)
        role_name = role_select(instance_type)
        if role_name == 2:  # 进入账户注册环节, 仅适用与学员 讲师
            instance_type.register()
        else:
            instance_type.control_operation(role_name)


def role_select(obj):
    return obj.auth()

