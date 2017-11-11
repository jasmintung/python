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
from core.db_handler import UserDataControl
from core.db_handler import StudentDataControl
from conf import settings
file_dst = settings.FILE_BASE


class StudentModule(object):
    def __init__(self):
        self.name = None
        self.school_name = None
        self.class_name = None

    def func_control(self, args):
        func_dict = {1: self.register_course_system, 2: self.check_personal_socre}
        if args in func_dict:
            instance_sm = SchoolModule()
            school_dict = instance_sm.get_school_list()
            print("请选择学校(根据编号)")
            for school in school_dict:
                print("编号: %d 学校: %s" % (school, school_dict[school]))
            usr_chose_school_id = int(input())
            if usr_chose_school_id in school_dict:
                self.school_name = school_dict[usr_chose_school_id]
                return func_dict[args]()
            else:
                print("编号输入错误")

    @login_deco(1)
    def auth(self):
        # 登陆
        instance_am = AuthModule(1)
        return instance_am.login()

    def register(self):  # 账户注册
        is_sure_to_register = input("是否进行注册? Y/N").strip()
        if is_sure_to_register == "Y":
            account = input("请输入用户名:")
            password = input("请输入密码:")
            student_dict = {}
            student_dict["id"] = "st00408"  # 这里根据/db/user_db/stid_db文件里面已存在学员ID进行ID分配
            student_dict["name"] = account
            student_dict["password"] = password
            student_dict["Register"] = 0
            write_database_dst = "%s/%s/%s/%s" % (file_dst["path"], file_dst["dir_name3"], file_dst["dir_name3_1"], account)
            instance_uc = UserDataControl(write_database_dst)
            instance_uc.create(student_dict)
        elif is_sure_to_register == "N":
            pass
        else:
            pass

    def control_operation(self, name):
        self.name = name
        operation_info = """
                        请选择:
                        1. 开始选课
                        2. 查询成绩
                        """
        print(operation_info)
        input_operation = int(input().strip(">>"))
        if self.func_control(input_operation):
            pass
        else:
            print("选择不正确")

    def register_course_system(self):  # 择校择班后进行 注册
        """
        *args: 里面有两个元素: 学校 班级
        :return: 注册结果
        """
        # 先判断是否已经注册成功,注册成功的前提是选校,选班,缴费后
        student_dst = "%s/%s/%s/%s" % (file_dst["path"], file_dst["dir_name3"], file_dst["dir_name3_1"], self.name)
        instance_st = UserDataControl(student_dst)
        student_dict = instance_st.read()
        if student_dict["Register"] == 1:
            print("您已选过课程了")
        else:
            # 选择学校,班级
            class_list = ClassModule.get_class_list(self.school_name)
            print(class_list[:])
            print("请选择班级(根据班级全名)")
            usr_chose_class = input()
            if usr_chose_class in class_list:
                print("选择正确,是否注册当前班级?")
                is_register = input("Y/N")
                if is_register == 'Y':
                    self.class_name = usr_chose_class
                    self.payment()
                else:
                    print("\033[36;1m您放弃注册,数据将丢失!\033[0m")
            else:
                print("\033[33;1m选班输入错误\033[0m")

    def payment(self):
        # 注册后交学费,交学费后才把 账户数据库 中的注册标识置1
        """

        :return:
        """
        sure_to_pay = input("是否缴费? Y/N")
        if sure_to_pay == "Y":
            student_list = []
            student_list[0] = self.name
            student_list[1] = self.class_name
            write_course_file_student = {}
            write_course_file_student[self.school_name]["0013"] = student_list
            instance_st_data = StudentDataControl()
            instance_st_data.read()
            instance_st_data.merge_dicts(write_course_file_student)
            instance_st_data.create()
        elif sure_to_pay == "N":
            print("\033[36;1m您未完成缴费,数据将丢失!\033[0m")

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
        pass

    def get_student_list(self):
        # 获取学员列表
        pass