# -*-coding=utf-8-*-
__author__ = 'zhangtong'
'''
Contact: puzexiong@163.com
'''
from conf import settings
file_dst = settings.FILE_BASE
from core.db_handler import SchoolDataControl
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
    def __init__(self, args):
        self.school_name = args
        self.school_data = {}
        self.obj = None
    schoo_id = 0
    ccsys_school_dst = "%s/%s/%s" % (file_dst["path"], file_dst["dir_name2"], file_dst["school_file_name"])

    def check_exists(self):
        # 检查要创建的学校是否已经存在
        is_exists = False
        if self.school_data is not None:
            for school_id in self.school_data:
                if self.school_name == self.school_data[school_id]:  # 这里进行数据查询
                    is_exists = True
        return is_exists

    def add_school(self):
        # 新增学校
        school_dict = {}
        if self.school_data is None:
            print("首次添加学校哦!")
            SchoolModule.schoo_id = 1
            school_dict[SchoolModule.schoo_id] = self.school_name
            self.obj.set_school_data(school_dict)
        else:
            SchoolModule.schoo_id = len(self.school_data) + 1
            self.school_data[SchoolModule.schoo_id] = self.school_name
            self.obj.set_school_data(self.school_data)
        self.obj.create(None)
        return 0

    def get_school_name(self):
        return self.school_name

    def set_school_name(self, school_name):
        self.school_name = school_name

    def get_school_data(self):
        return self.school_data

    def search_school_data(self):
        instance_sc = SchoolDataControl(SchoolModule.ccsys_school_dst)
        self.obj = instance_sc
        instance_sc.read()
        self.school_data = instance_sc.get_school_data()

