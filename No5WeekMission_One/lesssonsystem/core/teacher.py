# -*-coding=utf-8-*-
__author__ = 'zhangtong'
'''
Contact: puzexiong@163.com
'''
from conf import settings
# 讲师类
# 讲师账号数据结构(唯一编号,姓名, 注册标识) 存放在user_db/teacher_db/tc00408文件里面
dict1 = {"id": "tc00408", "name": "马化腾", "password": "654321", "Register": 0}
# 选课数据库讲师表
dict2 = {"北京": ["Alex", "武配齐"],
         "上海": ["马化腾", "甄子丹"]}
from core.auth import login_deco
from core.auth import AuthModule
from core.school import SchoolModule
from core.classes import ClassModule
from core.student import StudentModule
from core.db_handler import UserDataControl
from core.db_handler import TeacherDataControl
from core.db_handler import ClassDataControl
from core.db_handler import SchoolDataControl
from core.db_handler import StudentDataControl
from conf import settings
file_dst = settings.FILE_BASE


class TeacherModule(object):
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
        instance_am = AuthModule(2)
        return instance_am.login()

    def register(self):  # 账户注册
        is_sure_to_register = input("是否进行注册? Y/N").strip()
        if is_sure_to_register == "Y":
            account = input("请输入用户名:")
            password = input("请输入密码:")
            teacher_dict = {}
            teacher_dict["id"] = "tc00408"  # 这里根据/db/user_db/tcid_db文件里面讲师已存在ID进行ID分配
            teacher_dict["name"] = account
            teacher_dict["password"] = password
            teacher_dict["Register"] = 0
            write_database_dst = "%s/%s/%s/%s" % (file_dst["path"], file_dst["dir_name3"], file_dst["dir_name3_2"], account)
            instance_uc = UserDataControl(write_database_dst)
            instance_uc.create(teacher_dict)
        elif is_sure_to_register == "N":
            pass
        else:
            pass

    def control_operation(self, name):
        self.name = name
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
        instance_tc_data_c = TeacherDataControl()
        instance_tc_data_c.read()
        for school in instance_tc_data_c.teacher_data:
            print(school)
        usr_chose_school_name = input("请选择校区:")
        if usr_chose_school_name in instance_tc_data_c.teacher_data:  # 判断讲师是否已经在被管理员创建关联的学校里面
            if self.name in instance_tc_data_c[usr_chose_school_name]:
                instance_cs_data_c = ClassDataControl()
                instance_cs_data_c.read()
                for class_name in instance_cs_data_c.class_data[usr_chose_school_name]:
                    print(class_name)
                print("请选择班级(根据班级全名)")
                usr_chose_class_name = input()
                if usr_chose_class_name in instance_cs_data_c.class_data[usr_chose_school_name]:
                    print("选择完成")
                    # 更新 选课数据库班级表, 更新 选课数据库讲师表
                    instance_cs_data_c.merge_dicts(usr_chose_school_name, usr_chose_class_name, "讲师", self.name)
                else:
                    print("\033[36;1m班级输入不正确\033[0m")
            else:
                print("\033[36;1m无法选择该校区班级,请重新选择!\033[0m")
        else:
            print("\033[36;1m校区选择不正确!\033[0m")

    def view_students_info(self, *args):  # 浏览学员信息(根据学校总览, 根据班级浏览暂时未开发完成)
        instance_sc_data_c = SchoolDataControl()
        school_info_dict = instance_sc_data_c.school_data
        for school_id in school_info_dict:
            print(school_info_dict[school_id])
        usr_chose_school = int(input("请输入要查看的学校(根据编号):"))
        if usr_chose_school in school_info_dict:
            print("1: 校浏览, 2: 班级浏览")
            usr_chose = input("请选择").strip(">>")
            if usr_chose == 1:
                instance_st_data_c = StudentDataControl()
                student_info_dict = instance_st_data_c.student_data
                print(student_info_dict)
            elif usr_chose == 2:
                pass
        else:
            print("\033[34;1m选择的学校不存在!\033[0m")

    def give_student_score(self, *args):  # 给学员打分, 暂时未开发完成
        pass
