from db import TablesInit
from core import db_handler, roleBase


def verify(name, password):
    db = TablesInit.getSQLDBHandler()
    db_handle = db_handler.DBControle(db, name, password)
    result, role_info = db_handle.verify()
    if result == 1:
        t_instance = roleBase.Teacher(db_handle, name, password)
        teacher_func_dict = {'1': t_instance.create_classes, '2': t_instance.create_class_records,
                             '3': t_instance.modify_class_records, '4': t_instance.delete_class_records}

        while True:
            notice = """
            1、创建班级    2、创建上课记录
            3、修改上课记录 4、删除上课记录
            5、退出
            """
            print(notice)
            choice = input("请选择操作:").strip()
            if choice in [x+1 for x in range(5)]:
                if choice == '9':
                    break
                else:
                    teacher_func_dict[choice]()
        else:
            print("\033[31;1m选择错误,请重新选择\033[0m")
    elif result == 2:
        s_instance = roleBase.Student(db_handle, name, password, role_info[3])
        student_func_dict = {'1': s_instance.commit_mission, '2': s_instance.view_score}
        while True:
            notice = """
            1、提交作业     2、查看成绩
            3、退出
            """
            print(notice)
            choice = input("请选择操作:").strip()
            if choice in [x+1 for x in range(3)]:
                if choice == '3':
                    break
                else:
                    student_func_dict[choice]()
    else:
        sure_enroll = input("是否注册?Y/N:").strip()
        if sure_enroll == 'Y':
            name = input("请输入用户名:").strip()
            password = input("请输入密码:").strip()
            role_type = input("学员还是讲师?0:学员 1:讲师:").strip()
            if role_info in [0, 1]:
                role_instance = roleBase.Role(db_handle, name, password)
                role_instance.enroll(role_info)
        elif sure_enroll == 'N':
            pass
        else:
            print("\033[31;1m用户名或密码错误!\033[0m")


def run():
    notice_info = """
    *******登陆课堂系统*******
    """
    print(notice_info)
    while True:
        name = input("请输入用户名:").strip()
        password = input("请输入密码:").strip()
        verify(name, password)
