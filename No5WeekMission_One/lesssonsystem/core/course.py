# -*-coding=utf-8-*-
__author__ = 'zhangtong'
'''
Contact: puzexiong@163.com
'''
from conf import settings
file_dst = settings.FILE_BASE
from core.db_handler import CourseDataControl
# 课程类

# 课程类数据结构
dict1 = {"北京": {"C++": {"学时": 12, "学费": 6000}, "python": {"学时": 6, "学费": 8000}},
         "深圳": {"java script": {"学时": 3, "学费": 4000}, "unity3D": {"学时": 5, "学费": 8000}}}


class CourseModule(object):
    def __init__(self, args):
        self.school_name = args
        self.course_name = None
        self.course_data = {}
        self.obj = None

    ccsys_course_dst = "%s/%s/%s" % (file_dst["path"], file_dst["dir_name2"], file_dst["course_file_name"])

    def check_exists(self):
        is_exists = False
        if self.course_data is not None:
            if self.school_name in self.course_data:
                if self.course_name in self.course_data[self.school_name]:
                    is_exists = True
        return is_exists

    def get_current_course_list(self):
        # 获取XX学校当前课程列表并返回课程当前总数
        print(self.school_name)
        length = 0
        return length

    def add_course(self):
        # 增加课程

        course_dict = {}
        course_school_dict = {}
        while True:
            course_info_dict = {}
            course_name = input("输入课程名称:")
            course_cycle = input("输入课程周期(月):")
            course_price = input("输入课程价格(元):")
            course_info_dict["学时"] = course_cycle
            course_info_dict["学费"] = course_price
            course_dict[course_name] = course_info_dict
            next_operation = input("继续增加课程回车,否则输入'Q'退出")
            if next_operation == "Q":
                break
        course_school_dict[self.school_name] = course_dict
        if self.course_data is None:
            print("首次创建课程哦!")
            self.obj.set_course_data(course_school_dict)
        else:
            if self.school_name in self.course_data:  # 这个校区已经创建过课程拉
                self.course_data.update(course_school_dict)
            else:
                self.course_data[self.school_name] = course_dict
            self.obj.set_course_data(self.course_data)
        self.obj.create(None)

    def search_course_data(self):
        instance_cs = CourseDataControl(CourseModule.ccsys_course_dst)
        self.obj = instance_cs
        instance_cs.read()
        self.course_data = instance_cs.get_course_data()

    def set_course_name(self, course_name):
        self.course_name = course_name
