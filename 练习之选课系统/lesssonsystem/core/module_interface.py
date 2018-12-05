from core.student import StudentModule
from core.teacher import TeacherModule
from core.school import SchoolModule
from core.classes import ClassModule
from core.course import CourseModule


"""
提供各个角色类初始化接口
"""


class module_create(object):
    def __init__(self, args):
        self.func_number = args
        self.obj = None
        self.init_args = None

    def create_module(self):
        if self.func_number == 1:
            pass
            # self.obj = AdminModule()
        elif self.func_number == 5:
            print("实例化班级类")
            self.obj = ClassModule(self.init_args)
        elif self.func_number == 6:
            print("实例化课程类")
            self.obj = CourseModule(self.init_args)
        elif self.func_number == 4:
            print("实例化学校类")
            self.obj = SchoolModule(self.init_args)
        elif self.func_number == 2:
            print("实例化学生类")
            self.obj = StudentModule(self.init_args)
        elif self.func_number == 3:
            print("实例化讲师类")
            self.obj = TeacherModule(self.init_args)

    def get_module_obj(self):
        """
        获得各个角色类的实例化对象
        :return:
        """
        return self.obj

    def set_module_init_args(self, args):
        """
        给各个角色类的初始化参数
        :param args:
        :return:
        """
        self.init_args = args



