# -*-coding=utf-8-*-
__author__ = 'zhangtong'
'''
Contact: puzexiong@163.com
'''
# 学校类
# 学校类数据结构
dict1 = {1: "北京", 2: "广州", 3: "深圳", 4: "上海", 5: "大连", 6: "杭州", 7: "成都", 8: "武汉", 9: "沈阳"}

list1 = ["1312", "1312", "fasfasd"]
# usr_input = input()
# if usr_input in list1:
#     print("yes")
# else:
#     print("no")


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

    def get_school_list(self):
        school_list = []
        return school_list

