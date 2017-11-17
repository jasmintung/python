import os
import pickle
import json
import copy
from conf import settings
file_dst = settings.FILE_BASE


class DataControl(object):

    def __init__(self, args):
        self.dst = None
        self.write_file_data = None

    def create(self, args):  # 创建
        with open(self.dst, "w", encoding="utf-8") as wf:
            pickle.dump(self.write_file_data, wf)

    def read(self):  # 读取
        print("Basice Read Func!")

    def update(self):  # 更新
        pass

    def account_auth(self, *args):  # 账户检测
        pass

    def merge_dicts(self, x):
        pass
# 针对db/admin_db/admin_account文件里的管理员信息


class AdminDataControl(DataControl):

    def __init__(self, args):
        super(AdminDataControl, self).__init__(args)

    def create(self, args):
        pass

    def account_auth(self, *args):
        """

        :param args: 0: 用户名,1: 密码
        :return: 登陆是否成功表示0: 登陆成功, 1: 登陆失败
        """
        login_statue = 1
        admin_db_dst = "%s/%s/%s" % (file_dst["path"], file_dst["dir_name1"], file_dst["admin_file_name"])
        if os.path.exists(admin_db_dst) is True:
            with open(admin_db_dst, "r", encoding="utf-8") as rf:
                admin_account_data = json.load(rf)
                for i in admin_account_data:
                    admin_list = admin_account_data.get(i)
                    if args[0] in admin_list and args[1] in admin_list:
                        login_statue = 0
        else:
            print("文件不存在!")
        return login_statue

# 针对db/user_db/目录下的学生,讲师注册信息


class UserDataControl(DataControl):

    def __init__(self, args):
        super(UserDataControl, self).__init__(args)
        self.user_data = None
        self.dst = args

    def account_auth(self, *args):
        """

        :param args: 0: 用户类型（1:学生、2:讲师）1: 用户名,2: 密码
        :return: 登陆是否成功表示0: 登陆成功, 1 or 2: 登陆失败
        """
        login_statue = -1
        user_db_dst = ""
        user_db_dir = "%s/%s" % (file_dst["path"], file_dst["dir_name3"])
        if args[0] == 1:  # 学生
            user_db_dst = "%s/%s/%s" % (user_db_dir, file_dst["dir_name3_1"], args[1])
        elif args[0] == 2:  # 讲师
            user_db_dst = "%s/%s/%s" % (user_db_dir, file_dst["dir_name3_2"], args[1])
        if os.path.exists(user_db_dst) is True:  # 用户存在
            with open(user_db_dst, "rb") as rf:
                user_data = pickle.load(rf)
                if user_data["name"] == args[1] and user_data["password"] == args[2]:
                    login_statue = 0  # 账户匹配
                elif user_data["name"] == args[1] and user_data["password"] != args[2]:
                    login_statue = 1  # 密码不对
        else:
            login_statue = 2  # 账户不存在
        return login_statue

    def check_user_exists(self):
        """
        查看账户是否存在
        :return:
        """
        print(self.dst)
        return os.path.exists(self.dst) is True  # 用户存在

    def create(self, args):
        """

        :param args: args表示传入的要创建的人员信息
        :return:
        """
        with open(self.dst, "wb") as wf:
            if self.user_data is None:
                print(args)
                pickle.dump(args, wf)
            else:
                print(self.user_data)
                pickle.dump(self.user_data, wf)

    def read(self):
        with open(self.dst, "rb") as rf:
            if os.path.getsize(self.dst) != 0:
                self.user_data = pickle.load(rf)

    def get_user_data(self):
        return self.user_data

    def set_user_data(self, args):
        self.user_data = args

# 以下针对db/course_choosing_sys_db/目录下的数据信息


class SchoolDataControl(DataControl):  # 学校类

    def __init__(self, args):
        super(SchoolDataControl, self).__init__(args)
        self.school_data = None
        self.dst = args

    def get_school_data(self):
        return self.school_data

    def set_school_data(self, args):
        self.school_data = args

    def create(self, args):
        """
        创建学校
        :return: 创建结果
        """
        with open(self.dst, "wb") as wf:
            print(self.school_data)
            pickle.dump(self.school_data, wf)

    def read(self):
        """
        获取学校列表
        :param args:
        :return: 学校列表
        """
        if os.path.exists(self.dst) is True:
            with open(self.dst, "rb") as rf:
                if os.path.getsize(self.dst) != 0:
                    self.school_data = pickle.load(rf)


class ClassDataControl(DataControl):  # 班级类

    def __init__(self, args):
        super(ClassDataControl, self).__init__(args)
        self.class_data = None
        self.write_file_data = None
        self.dst = args

    def get_class_data(self):
        return self.class_data

    def set_class_data(self, args):
        self.class_data = args

    def create(self, args):
        """
        创建班
        :return:
        """
        with open(self.dst, "wb") as wf:
            print(self.class_data)
            pickle.dump(self.class_data, wf)

    def read(self):
        """
        获取班级文件
        """
        with open(self.dst, "rb") as rf:
            if os.path.getsize(self.dst) != 0:
                self.class_data = pickle.load(rf)
                print(self.class_data)

    def merge_dicts(self, *args):
        """

        :param args: 要合并信息
        :return:
        """
        self.class_data[args[0]][args[1]][args[2]].append(args[3])
        self.write_file_data = self.class_data


class CourseDataControl(DataControl):  # 课程类
    course_id = 0

    def __init__(self, args):
        super(CourseDataControl, self).__init__(args)
        self.course_data = None
        self.dst = args

    def get_course_data(self):
        return self.course_data

    def set_course_data(self, args):
        self.course_data = args

    def create(self, args):
        """
        创建课程
        :return:
        """
        with open(self.dst, "wb") as wf:
            pickle.dump(self.course_data, wf)

    def read(self):
        """
        获取课程列表
        :param args: args0: 学校, args1: 0 or 1
        :return:0: 课程列表, 1 整个文件内容
        """
        with open(self.dst, "rb") as rf:
            if os.path.getsize(self.dst) != 0:
                self.course_data = pickle.load(rf)
                print(self.course_data)


class StudentDataControl(DataControl):  # 学员类

    def __init__(self, args):
        super(StudentDataControl, self).__init__(args)
        self.student_data = None
        self.school_name = None
        self.dst = args

    def create(self, args):
        """
        创建学生
        :param args:文件地址
        :return:
        """
        with open(self.dst, "wb") as wf:
            print(self.student_data)
            pickle.dump(self.student_data, wf)

    def set_student_data(self, args):
        self.student_data = args

    def get_student_data(self):
        return self.student_data

    def read(self):
        """
        获取整个文件内容
        """
        with open(self.dst, "rb") as rf:
            if os.path.getsize(self.dst) != 0:
                self.student_data = pickle.load(rf)
                print(self.student_data)


class TeacherDataControl(DataControl):  # 讲师类

    def __init__(self, args):
        super(TeacherDataControl, self).__init__(args)
        self.teacher_data = None
        self.dst = args

    def get_teacher_data(self):
        return self.teacher_data

    def set_teacher_data(self, args):
        self.teacher_data = args

    def create(self, args):
        """
        创建讲师
        :param args: 0: 学校, 1: 讲师
        :return: 创建结果
        """
        with open(self.dst, "wb") as wf:
            print(self.teacher_data)
            pickle.dump(self.teacher_data, wf)

    def read(self):
        """
        获取讲师整个文件内容
        """
        if os.path.exists(self.dst) is True:
            with open(self.dst, "rb") as rf:
                file_length = os.path.getsize(self.dst)
                if file_length != 0:
                    self.teacher_data = pickle.load(rf)
                    print(self.teacher_data)

