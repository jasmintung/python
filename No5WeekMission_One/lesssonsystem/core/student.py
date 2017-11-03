# -*-coding=utf-8-*-
__author__ = 'zhangtong'
'''
Contact: puzexiong@163.com
'''
# 学员类
# 学员类数据结构
# 账号数据库(唯一编号,姓名, 注册标识)
dict1 = {"id": "st00408", "name": "杰森斯坦森", "password": "123456", "Register": 0}
# 选课数据库学员表
dict2 = {"大连": {"0001": ["Jack", "一班"], "0002": ["李老大", "二班"]},
         "广州": {"0001": ["习大大", "一班"], "0002": ["王大雷", "二班"]}}

from core.auth import AuthModule
from core.auth import login_deco
from core.school import SchoolModule
from core.classes import ClassModule


class StudentModule(object):
    def __init__(self):
        self.name = None

    @login_deco(1)
    def auth(self):
        # 登陆
        instance_am = AuthModule()
        self.name = instance_am.login()
        if self.name:
            self.chose_class()
        else:
            pass

    def register(self, *args):  # 择校择班后进行注册
        """
        *args: 里面有两个元素: 学校 班级
        :return: 注册结果
        """
        # 选课数据库里面去检查是否已经选过课了,然后告知是否缴学费

        has_pay = False
        if has_pay is True:
            self.payment()

    def payment(self):
        # 注册后交学费,交学费后才把 账户数据库 中的注册标识置1
        """
        更新 账户数据库 选课数据库学员表 和 选课数据库班级表
        :return:
        """

    def chose_class(self):
        # 选择学校,班级
        instance_sm = SchoolModule()
        print("请选择学校(根据编号)")
        school_dict = instance_sm.get_school_list()
        for school in school_dict:
            print("编号: %d 学校: %s" % (school, school_dict[school]))
        usr_chose_school_id = input()

        if usr_chose_school_id in school_dict:
            class_list = ClassModule.get_class_list(school_dict[usr_chose_school_id])
            print(class_list[:])
            print("请选择班级(根据班级全名)")
            usr_chose_class = input()
            if usr_chose_class in class_list:
                print("选择正确,是否注册?")
                is_register = input("Y/N")
                if is_register == 'Y':
                    self.register(school_dict[usr_chose_school_id], usr_chose_class)
                else:
                    print("先不注册")

    def check_exists(self, student_name):
        # 检查要创建的学员是否已经存在dict1
        is_exists = False
        # 数据库查询
        return is_exists

    def add_student(self, *args):
        # 创建学员
        pass

    def check_personal_socre(self):
        # 查阅个人成绩
        pass

    def get_student_list(self):
        # 获取学员列表
        pass