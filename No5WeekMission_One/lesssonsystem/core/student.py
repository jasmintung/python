# -*-coding=utf-8-*-
__author__ = 'zhangtong'
'''
Contact: puzexiong@163.com
'''
# 学员类
# 学员类数据结构
dict1 = {"大连": {"0001": ["Jack", "一班"], "0002": ["李老大", "二班"]},
         "广州": {"0001": ["习大大", "一班"], "0002": ["王大雷", "二班"]}}


class StudentModule(object):
    def __init__(self, school_name, class_name):
        self.school_name = school_name
        self.class_name = class_name

    def register(self):
        # 注册
        pass

    def payment(self):
        # 交学费
        pass

    def chose_class(self):
        # 选择班级
        pass

    def check_exists(self, student_name):
        # 检查要创建的学员是否已经存在dict1
        is_exists = False
        # 数据库查询
        return is_exists

    def add_student(self, *args):
        # 创建学员
        pass