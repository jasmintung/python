from core.student import StudentModule
from core.teacher import TeacherModule
from core.admin import AdminModule


def run():
    # 程序主入口
    while True:
        print("***欢迎使用选课系统***")
        charactor = int(input("请选择登陆角色: 1: 学生 2: 讲师 8: 管理员"))
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
        role_select(instance_type)


def role_select(obj):
    obj.auth()

