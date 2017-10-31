# -*-coding=utf-8-*-
__author__ = 'zhangtong'
'''
Contact: puzexiong@163.com
'''
# 课程类

# 课程类数据结构
dict1 = {"北京": {"0001": ["C++", "1年", "6000"], "0002": ["python", "2年", "8000"]},
         "杭州": {"0001": ["C#", "1年", "3000"], "0002": ["JAVA", "3年", "10000"]}}


class CourseModule(object):
    def __init__(self, school_name):
        self.school_name = school_name

    def check_exists(self):
        # 检查要创建的课程是否已经存在dict1
        is_exists = False
        # 数据库查询
        return is_exists

    def get_current_course_list(self):
        # 获取XX学校当前课程列表并返回课程当前总数
        print(self.school_name)
        length = 0
        return length

    def add_course(self, *args):
        # 增加课程
        pass
