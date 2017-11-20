# -*-coding=utf-8-*-
__author__ = 'zhangtong'
'''
Contact: puzexiong@163.com
'''
# 管理员类

from core.auth import login_deco
from core.auth import AuthModule
from core.module_interface import module_create
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

    def quit(self):
        exit()

    def func_control(self, args):
        func_dict = {1: self.create_school, 2: self.create_class,
                     3: self.create_teacher, 4: self.create_course, 0: self.quit}
        if args == 0:
            func_dict[0]()
        else:
            if args in func_dict:
                if args == 1:
                    func_dict[args](0)
                else:
                    func_dict[args]()
            else:
                print("\033[33;1m没有这个选项!\033[0m")

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
            input_operation = input()
            if input_operation.isdigit():
                self.func_control(int(input_operation))
            else:
                print("\033[33;1m输入不正确!\033[0m")

    def create_school(self, args):  # OK
        """

        :param args: 0 表示创建时调用,1表示检查时调用
        :return:
        """
        # 创建学校
        school_name = input("输入学校名称:")
        instance_module = module_create(4)
        instance_module.set_module_init_args(school_name)
        instance_module.create_module()
        instance_t_school = instance_module.get_module_obj()
        instance_t_school.search_school_data()
        result = instance_t_school.check_exists()
        if args == 0:
            if result is True:
                print("\033[32;1m学校已经存在了,不能重复添加!\033[0m")
            else:
                instance_t_school.add_school()
        else:
            if result is False:
                print("\033[33;1m学校不存在,无法创建班级!\033[0m")
        self.school_name = school_name
        return result

    def create_class(self):  # OK
        # 创建班级
        if self.create_school(1) is True:
            instance_module = module_create(5)
            instance_module.set_module_init_args(self.school_name)
            instance_module.create_module()
            instance_t_class = instance_module.get_module_obj()
            instance_t_class.search_class_data()
            instance_t_class.add_class()

    def create_teacher(self):
        # 创建讲师
        if self.create_school(1) is True:
            instance_module = module_create(3)
            instance_module.set_module_init_args(self.school_name)
            instance_module.create_module()
            instance_t_teacher = instance_module.get_module_obj()
            instance_t_teacher.search_teacher_data()
            instance_t_teacher.add_teacher()

    def create_course(self):
        # 创建课程
        if self.create_school(1) is True:
            instance_module = module_create(6)
            instance_module.set_module_init_args(self.school_name)
            instance_module.create_module()
            instance_t_course = instance_module.get_module_obj()
            instance_t_course.search_course_data()
            instance_t_course.add_course()

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
