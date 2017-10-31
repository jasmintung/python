# -*-coding=utf-8-*-
__author__ = 'zhangtong'
'''
Contact: puzexiong@163.com
'''
# 学员类
# 学员类数据结构
# 账号数据库(唯一编号,姓名, 注册标识)
dict1 = {"0001": ["杰森斯坦森", 0], "0002": ["汤姆克鲁斯", 0], "0003": ["大卫罗宾逊", 0]}
# 选课数据库
dict2 = {"大连": {"0001": ["Jack", "一班"], "0002": ["李老大", "二班"]},
         "广州": {"0001": ["习大大", "一班"], "0002": ["王大雷", "二班"]}}
from core.auth import AuthModule
from core.auth import login_deco


class StudentModule(object):
    def __init__(self):
        pass

    @login_deco(1)
    def auth(self):
        # 登陆
        instance_am = AuthModule()
        instance_am.login()

    def register(self):
        # 注册
        pass

    def payment(self):
        # 交学费
        pass

    def chose_class(self):
        # 选择学校,班级 判断是否有注册
        pass

    def check_exists(self, student_name):
        # 检查要创建的学员是否已经存在dict1
        is_exists = False
        # 数据库查询
        return is_exists

    def add_student(self, *args):
        # 创建学员
        pass