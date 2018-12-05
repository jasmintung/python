# -*-coding=utf-8-*-
__author__ = 'zhangtong'
import sys
from conf import settings
file_dst = settings.FILE_BASE
from core.school import SchoolModule
from core.user_id_control import UserIdControlModule
from core.db_handler import UserDataControl
from core.classes import ClassModule
from core.db_handler import StudentDataControl
from core.auth import AuthModule
from core.auth import login_deco

'''
Contact: puzexiong@163.com
'''
# 学员类
# 学员类数据结构
# 账号数据库(唯一编号,姓名, 注册标识)
# dict1 = {"id": "st00408", "name": "杰森斯坦森", "password": "123456", "Register": 0, "score": 0}
# 选课数据库学员表
# dict2 = {"大连": {"st00408": {"姓名": "Jack", "班级": "一班"}, "st00409": {"姓名": "李老大", "班级": "二班"}},
#          "广州": {"st00001": {"姓名": "习大大", "班级": "一班"}, "st00301": {"姓名": "王大雷", "班级": "二班"}}}


class StudentModule(object):
    def __init__(self):
        self.student_name = None
        self.school_name = None
        self.class_name = None
        self.st_login_result = None
        self.st_id = 0
        self.student_data = {}
    ccsys_school_dst = "%s/%s/%s" % (file_dst["path"], file_dst["dir_name2"], file_dst["school_file_name"])
    ccsys_student_dst = "%s/%s/%s" % (file_dst["path"], file_dst["dir_name2"], file_dst["student_file_name"])

    def func_control(self, args):
        func_dict = {1: self.register_course_system, 2: self.check_personal_socre, 0: self.quit}
        if args == 0:
            func_dict[0]()
        else:
            if args in func_dict:
                instance_sm = SchoolModule(StudentModule.ccsys_school_dst)
                instance_sm.search_school_data()
                school_dict = instance_sm.get_school_data()
                if school_dict is None:
                    print("目前还没有学校可以选择!")
                else:
                    print("请选择学校(根据编号)")
                    for school in school_dict:
                        print("编号: %d 学校: %s" % (school, school_dict[school]))
                    usr_chose_school_id = int(input())
                    if usr_chose_school_id in school_dict:
                        self.school_name = school_dict[usr_chose_school_id]
                        return func_dict[args]()
                    else:
                        print("\033[33;1m学校选择错误!\033[0m")
            else:
                print("\033[33;1m编号输入错误!\033[0m")

    def login_result(self):
        return self.st_login_result

    @login_deco(1)
    def auth(self):
        # 登陆
        instance_am = AuthModule(1)
        self.st_login_result = instance_am.login()

    def quit(self):
        print("退出程序!")
        sys.exit()

    def register(self):  # 账户注册
        is_sure_to_register = input("是否进行注册? Y/N").strip()
        if is_sure_to_register == "Y":
            account = input("请输入用户名:")
            password = input("请输入密码:")
            student_dict = {}
            instance_userId_Control = UserIdControlModule(None)
            instance_userId_Control.assigned_id(0)
            st_id = "ST" + str(instance_userId_Control.get_id()).rjust(5, "0")  # 这里根据/db/user_db/stid_db文件里面已存在学员ID进行ID分配
            instance_userId_Control.set_id_data(st_id)
            instance_userId_Control.create_id()  # 创建新的ID并写入ID文件
            student_dict["id"] = st_id
            student_dict["name"] = account
            student_dict["password"] = password
            student_dict["Register"] = 0
            student_dict["score"] = 0
            write_database_dst = "%s/%s/%s/%s" % (file_dst["path"], file_dst["dir_name3"], file_dst["dir_name3_1"], account)
            instance_uc = UserDataControl(write_database_dst)
            instance_uc.create(student_dict)  # 用户个人信息文件创建
        elif is_sure_to_register == "N":
            pass
        else:
            pass

    def control_operation(self, name):
        while True:
            self.student_name = name
            operation_info = """
                            请选择:
                            1. 开始选课
                            2. 查询成绩
                            0. 退出
                            """
            print(operation_info)
            input_operation = int(input().strip(">>"))
            self.func_control(input_operation)

    def register_course_system(self):  # 择校择班后进行 注册
        # 先判断是否已经注册成功,注册成功的前提是选校,选班,缴费后
        student_dst = "%s/%s/%s/%s" % (file_dst["path"], file_dst["dir_name3"], file_dst["dir_name3_1"], self.student_name)
        print("student_dst:", student_dst)
        instance_st = UserDataControl(student_dst)
        instance_st.read()
        student_dict = instance_st.get_usr_data()
        print("学员:", student_dict)
        self.st_id = student_dict["id"]
        if student_dict["Register"] == 1:
            print("您已选过课程了")
        else:
            # 选择学校,班级
            instance_cs = ClassModule(self.school_name)
            instance_cs.search_class_data()
            class_dict = instance_cs.get_class_data()
            print(class_dict)
            print("请选择班级(根据班级全名)")
            usr_chose_class = input()
            if usr_chose_class in class_dict[self.school_name]:
                print("选择正确,是否注册当前班级?")
                is_register = input("Y/N")
                if is_register == 'Y':
                    self.class_name = usr_chose_class
                    if self.payment() is True:
                        student_dict["Register"] = 1
                        instance_st.set_usr_data(student_dict)
                        instance_st.create(None)
                else:
                    print("\033[36;1m您放弃注册,数据将丢失!\033[0m")
            else:
                print("\033[33;1m选班输入错误\033[0m")

    def payment(self):
        # 注册后交学费,交学费后才把 账户数据库 中的注册标识置1
        """

        :return: True:缴费完成,False:缴费失败
        """
        pay_result = False
        sure_to_pay = input("是否缴费?缴费后无法重新选课了哦!!! Y/N")
        if sure_to_pay == "Y":
            student_dict = {}
            student_info_dict = {}
            write_file_dict = {}
            student_info_dict["姓名"] = self.student_name
            student_info_dict["班级"] = self.class_name
            student_dict[self.st_id] = student_info_dict
            write_file_dict[self.school_name] = student_dict
            instance_st_data = StudentDataControl(StudentModule.ccsys_student_dst)
            instance_st_data.read()
            self.student_data = instance_st_data.get_data()
            if self.student_data is None:
                print("\033[34;1m您是第一位报名课程的!\033[0m")
                instance_st_data.set_data(write_file_dict)
            else:
                self.student_data[self.school_name].update(write_file_dict[self.school_name])
                instance_st_data.set_data(self.student_data)
                print("\033[34;1m选课成功!\033[0m")
            instance_st_data.create(None)
            pay_result = True
        elif sure_to_pay == "N":
            print("\033[36;1m您未完成缴费,数据将丢失!\033[0m")
        else:
            print("\033[34;1m输入不正确!\033[0m")
        return pay_result

    def get_student_data(self):
        # 获取学员列表
        return self.student_data

    def search_student_data(self):
        instance_st = StudentDataControl(StudentModule.ccsys_student_dst)
        self.obj = instance_st
        instance_st.read()
        self.student_data = instance_st.get_data()

    def check_exists(self):
        # 检查要创建的学员是否已经存在dict1
        is_exists = False
        # 数据库查询
        return is_exists

    def add_student(self):
        # 创建学员
        pass

    def check_personal_socre(self):
        # 查阅个人成绩
        user_database_dst = "%s/%s/%s/%s" % (file_dst["path"], file_dst["dir_name3"], file_dst["dir_name3_1"], self.student_name)
        instance_ud = UserDataControl(user_database_dst)
        if instance_ud.check_user_exists() is True:
            instance_ud.read()
            student_data = instance_ud.get_usr_data()
            score = student_data.get("score")
            print("\033[34;1m您的成绩是: \033[0m", score)
        else:
            print("您的信息被删除了!")

