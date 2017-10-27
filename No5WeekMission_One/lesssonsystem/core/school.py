# -*-coding=utf-8-*-
__author__ = 'zhangtong'
'''
Contact: puzexiong@163.com
'''
# 学校类
# 学校类数据结构
dict1 = {"北京", "广州", "深圳", "上海", "大连", "杭州", "成都", "武汉", "沈阳"}
for key in dict1:
    print(key)


class SchoolModule(object):
    def __int__(self, name):
        self.name = name

    def check_exists(self):
        # 检查要创建的学校是否已经存在dict1
        is_exists = False
        if self.name == "北京":  # 这里进行数据查询
            is_exists = True
        return is_exists

    def add_school(self, name):
        # 新增学校
        self.name = name

    def get_school_name(self):
        return self.name
