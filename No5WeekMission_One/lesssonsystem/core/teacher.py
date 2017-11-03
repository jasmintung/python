# -*-coding=utf-8-*-
__author__ = 'zhangtong'
'''
Contact: puzexiong@163.com
'''
from conf import settings
# 讲师类
# 讲师类数据结构
# 账号数据库
dict1 = {"0001": "马化腾", "0002": "甄子丹", "0003": "袁隆平"}
# 选课数据库讲师表
dict2 = {"北京": ["Alex", "武配齐"],
         "上海": ["马化腾", "甄子丹"]}
from core.auth import login_deco
from core.auth import AuthModule
from core.school import SchoolModule
from core.classes import ClassModule
from core.student import StudentModule


class TeacherModule(object):
    conn_params = settings.FILE_BASE

    def __int__(self):
        self.name = None

    def func_control(self, args):
        func_dict = {1: self.go_to_class, 2: self.view_students_info, 3: self.give_student_score}
        if args in func_dict:
            instance_sm = SchoolModule()
            school_dict = instance_sm.get_school_list()
            print("请选择学校(根据编号)")
            for school in school_dict:
                print("编号: %d 学校: %s" % (school, school_dict[school]))
            usr_chose_school_id = int(input())
            if usr_chose_school_id in school_dict:
                return func_dict[args]()
            else:
                print("编号输入错误")

    @login_deco(2)
    def auth(self):
        # 登陆
        instance_am = AuthModule()
        self.name = instance_am.login()
        if self.name:
            operation_info = """
            请选择:
            1. 选择授课班级
            2. 浏览学员信息
            3. 考核
            """
            print(operation_info)
            input_operation = int(input().strip(">>"))
            if self.func_control(input_operation):
                pass
            else:
                print("选择不正确")

    def check_exists(self, args):
        # 检查要创建的讲师是否已经存在dict1
        is_exists = False
        # 数据库查询
        return is_exists

    def add_teacher(self, *args):  # 创建讲师
        pass

    def go_to_class(self, *args):  # 选择上课班级
        instance_cs = ClassModule()
        class_list = instance_cs.get_class_list()
        print("请选择班级(根据班级全名)")
        usr_chose_class_name = input()
        if usr_chose_class_name in class_list:
            print("选择完成")
            # 更新 选课数据库班级表, 更新 选课数据库讲师表
        else:
            print("班级输入不正确")

    def view_students_info(self, *args):  # 浏览学员信息(根据学校总览, 根据班级浏览)
        print("1: 校浏览, 2: 班级浏览")
        usr_chose = input("请选择").strip(">>")
        if usr_chose == 1:
            instance_st = StudentModule()
            student_info_dict = instance_st.get_student_list(args)
            print(student_info_dict)
        elif usr_chose == 2:
            instance_cs = ClassModule()
            class_list = instance_cs.get_class_list()
            print("请选择班级(根据班级全名)")
            usr_chose_class_name = input()
            if usr_chose_class_name in class_list:
                print(class_list[usr_chose_class_name]["学员"])

    def give_student_score(self, *args):  # 给学员打分
        pass
