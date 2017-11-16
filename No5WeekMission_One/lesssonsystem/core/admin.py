# -*-coding=utf-8-*-
__author__ = 'zhangtong'
'''
Contact: puzexiong@163.com
'''
# 管理员类

from core.db_handler import TeacherDataControl
from core.db_handler import ClassDataControl
from core.db_handler import SchoolDataControl
from core.db_handler import StudentDataControl
from core.db_handler import CourseDataControl
from core.auth import login_deco
from core.auth import AuthModule
from core.school import SchoolModule
from core.classes import ClassModule
from core.teacher import TeacherModule
from core.course import CourseModule
# 管理员数据结构
dict1 = {"0001": "admin1", "0002": "admin2", "0003": "admin3"}


class AdminModule(object):
    def __int__(self):
        self.school_name = None
        self.ad_login_result = None
    school_id = 1

    def login_result(self):
        return self.ad_login_result

    @login_deco(8)
    def auth(self):
        # 登陆
        instance_am = AuthModule(0)
        self.ad_login_result = instance_am.login()
        print(self.ad_login_result)

    def quit(self):
        exit()

    def func_control(self, args):
        func_dict = {1: self.create_school, 2: self.create_class,
                     3: self.create_teacher, 4: self.create_course, 0: self.quit}
        if args == 0:
            func_dict[0]()
        else:
            if args in func_dict:
                func_dict[args]()
            else:
                print("\033[33;1m选择错误!\033[0m")

    def control_operation(self, name):
        while True:
            self.name = name
            operation_info = """
                    请选择:
                    1. 创建学校
                    2. 创建班级
                    3. 创建讲师
                    4. 创建课程
                    0. 退出
                    """
            print(operation_info)
            input_operation = int(input().strip(">>"))
            self.func_control(input_operation)

    def create_school(self):  # OK
        # 创建学校
        school_name = input("输入学校名称:")
        instance_t_school = SchoolModule(school_name)
        instance_t_school.add_school()

    def create_class(self):  # OK
        # 创建班级
        school_name = input("输入学校名称:")
        instance_t_school = SchoolModule(school_name)
        instance_t_school.search_school_data()

        if instance_t_school.check_exists() is True:
            instance_t_class = ClassModule(school_name)
            instance_t_class.search_class_data()
            instance_t_class.add_class()
        else:
            print("\033[33;1m学校不存在,无法创建班级!\033[0m")

    def create_teacher(self):
        # 创建讲师
        school_name = input("输入学校名称:")
        instance_t_school = SchoolModule(school_name)
        instance_t_school.search_school_data()

        if instance_t_school.check_exists() is True:
            instance_t_teacher = TeacherModule(school_name)
            instance_t_teacher.search_teacher_data()
            instance_t_teacher.add_teacher()
        else:
            print("\033[33;1m学校不存在,无法创建讲师!\033[0m")

    def create_course(self):
        # 创建课程
        school_name = input("输入学校名称:")
        instance_t_school = SchoolModule(school_name)
        instance_t_school.search_school_data()

        if instance_t_school.check_exists() is True:
            instance_t_course = CourseModule(school_name)
            instance_t_course.search_course_data()
            instance_t_course.add_course()
        else:
            print("\033[33;1m学校不存在,无法创建课程!\033[0m")

    # def create_student(self):
    #     # 创建学员
    #     dict_student = {}
    #     school_name = input("请输入要操作的学校的名称:")
    #     class_name = input("请输入要操作的班级名称:")
    #     t_school = SchoolModule(school_name)
    #     if check_interface(t_school) is True:  # 学校存在
    #         t_class = ClassModule(school_name)
    #         if check_interface(t_class) is True:  # 班级存在
    #             t_student = StudentModule(school_name, class_name)
    #             id = 1  # 判断已有ID号
    #             dict_student_name = {}
    #             while True:
    #                 list_student_name = []
    #                 student_name = input("请输入学员姓名:")
    #                 if check_interface(t_student, student_name) is False:
    #                     # {"大连": {"0001": ["Jack", "一班"], "0002": ["李老大", "二班"]}}
    #                     student_id = str(id).rstrip(6, "0")
    #                     list_student_name.append(student_name)
    #                     list_student_name.append(class_name)
    #                     dict_student_name[student_id] = list_student_name
    #                     next_opreation = input("继续增加课程回车,否则输入'#'退出")
    #                     id += 1
    #                     if next_opreation == '#':
    #                         dict_student[school_name] = dict_student_name
    #                         t_student.add_student(dict_student)
    #                         break


def check_interface(obj, *args):  # 将不同类别的值重复检查操作做成接口,方便后期维护
    return obj.check_exists(args)
