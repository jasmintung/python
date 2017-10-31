# -*-coding=utf-8-*-
__author__ = 'zhangtong'
'''
Contact: puzexiong@163.com
'''
# 讲师类
# 讲师类数据结构
# 账号数据库
dict1 = {"0001": "马化腾", "0002": "甄子丹", "0003": "袁隆平"}
# 选课数据库
dict2 = {"北京": {"Alex": ["二班", "一班", "三班"], "武配齐": ["八班", "二班"]},
         "上海": {"马化腾": ["四班", "一班"], "甄子丹": ["五班", "二班"]}}
from core.auth import login_deco
from core.auth import AuthModule


class TeacherModule(object):
    def __int__(self):
        pass

    @login_deco(2)
    def auth(self):
        # 登陆
        instance_am = AuthModule()
        instance_am.login()

    def chose_class(self):
        # 讲师选择班级
        pass

    def view_student_list(self):
        # 查看班级学员列表
        pass

    def operation_student_score(self):
        # 操作学员成绩
        pass

    def check_exists(self, args):
        # 检查要创建的讲师是否已经存在dict1
        is_exists = False
        # 数据库查询
        return is_exists

    def add_teacher(self, *args):
        # 创建讲师
        pass