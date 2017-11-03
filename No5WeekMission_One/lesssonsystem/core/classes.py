# -*-coding=utf-8-*-
__author__ = 'zhangtong'
'''
Contact: puzexiong@163.com
'''
# 班级类
# 选课数据库班级表
dict1 = {"成都": {"一班": {"课程": ["JAVA", "Android", "Unity3D", "Python"],
                       "讲师": ["Alex", "Tom"]},
                "二班": {"课程": ["C++", "C#", "Go", "Python"],
                       "讲师": ["Jack", "Jmy"]}},
         "武汉": {"一班": {"课程": ["算法导论", "软件工程"], "讲师": ["Mobile", "Papa"]}}}


class ClassModule(object):
    def __int__(self, school_name):
        self.school_name = school_name

    def check_exists(self):  # 后面可考虑做成接口
        # 检查要创建的班级是否已经存在dict1
        is_exists = False
        # 数据库查询
        return is_exists

    def add_class(self, *args):  # 传进来的args是以key-value形式传进来
        # 创建班级
        pass

    def get_class_list(self, *args):  # args: 学校名字
        pass

