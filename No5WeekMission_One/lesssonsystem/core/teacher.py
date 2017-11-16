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
from core.db_handler import UserDataControl
from core.db_handler import TeacherDataControl
from core.db_handler import ClassDataControl
from core.db_handler import SchoolDataControl
from core.db_handler import StudentDataControl
from conf import settings
file_dst = settings.FILE_BASE


class TeacherModule(object):
    def __init__(self, args):
        self.obj = None
        self.school_name = args
        self.teacher_name = None
        self.tc_login_result = None
        self.teacher_data = {}

    ccsys_teacher_dst = "%s/%s/%s" % (file_dst["path"], file_dst["dir_name2"], file_dst["teacher_file_name"])

    def func_control(self, args):
        func_dict = {1: self.go_to_class, 2: self.view_students_info, 3: self.give_student_score, 0: self.quit}
        if args == 0:
            func_dict[0]()
        else:
            if args in func_dict:
                instance_sm = SchoolModule()
                instance_sm.search_school_data()
                school_dict = instance_sm.get_schoolModule_data()
                print(type(school_dict))
                if school_dict is None:
                    print("目前还没有学校可以选择!")
                else:
                    print(school_dict)
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
        return self.tc_login_result

    @login_deco(2)
    def auth(self):
        # 登陆
        instance_am = AuthModule(2)
        self.tc_login_result = instance_am.login()
        print(self.tc_login_result)

    def quit(self):
        exit()

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
        while True:
            self.teacher_name = name
            operation_info = """
                    请选择:
                    1. 选择授课班级
                    2. 浏览学员信息
                    3. 考核
                    0. 退出
                    """
            print(operation_info)
            input_operation = int(input().strip(">>"))
            self.func_control(input_operation)

    def check_exists(self):
        is_exists = False
        print(self.teacher_data)
        if self.teacher_data is not None:
            if self.school_name in self.teacher_data:
                if self.teacher_name in self.teacher_data[self.school_name]:  # 这里进行数据查询
                    is_exists = True
        return is_exists

    def go_to_class(self, *args):  # 选择上课班级
        instance_tc_data_c = TeacherDataControl()
        instance_tc_data_c.read()
        for school in instance_tc_data_c.teacher_data:
            print(school)
        usr_chose_school_name = input("请选择校区:")
        if usr_chose_school_name in instance_tc_data_c.teacher_data:  # 判断讲师是否已经在被管理员创建关联的学校里面
            if self.teacher_name in instance_tc_data_c[usr_chose_school_name]:
                instance_cs_data_c = ClassDataControl()
                instance_cs_data_c.read()
                for class_name in instance_cs_data_c.class_data[usr_chose_school_name]:
                    print(class_name)
                print("请选择班级(根据班级全名)")
                usr_chose_class_name = input()
                if usr_chose_class_name in instance_cs_data_c.class_data[usr_chose_school_name]:
                    print("选择完成")
                    # 更新 选课数据库班级表, 更新 选课数据库讲师表
                    instance_cs_data_c.merge_dicts(usr_chose_school_name, usr_chose_class_name, "讲师", self.teacher_name)
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

    def search_teacher_data(self):
        instance_tc = TeacherDataControl(TeacherModule.ccsys_teacher_dst)
        self.obj = instance_tc
        instance_tc.read()
        self.teacher_data = instance_tc.get_teacher_data()

    def add_teacher(self):
        dict_teacher = {}
        teacher_list = []
        while True:
            teacher_name = input("输入要在\"%s\"校区创建的\"讲师\"名字 回车继续 输入 'Q' 结束" % self.school_name)
            if teacher_name == 'Q':
                break
            teacher_list.append(teacher_name)

        if self.teacher_data is None:
            print("首次创建讲师哦!")
            dict_teacher[self.school_name] = teacher_list
            self.obj.set_teacher_data(dict_teacher)
        else:
            if self.school_name in self.teacher_data:  # 该校区已经创建过讲师
                self.teacher_data[self.school_name] = list(set(self.teacher_data[self.school_name] + teacher_list))
            else:
                self.teacher_data[self.school_name] = teacher_list
            self.obj.set_teacher_data(self.teacher_data)
        self.obj.create(None)

    def get_teacher_name(self):
        return self.teacher_name

    def set_teacher_name(self, teacher_name):
        self.teacher_name = teacher_name