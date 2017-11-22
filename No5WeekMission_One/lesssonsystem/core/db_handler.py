import os
import pickle
import json
import copy
from conf import settings
file_dst = settings.FILE_BASE


class DataControl(object):

    def __init__(self, args):
        print("DataControl")
        print(self)
        self.data = None
        self.dst = args

    def get_data(self):
        return self.data

    def set_data(self, args):
        self.data = args

    def read(self):
        print("Basice Read Func!")
        with open(self.dst, "rb") as rf:
            if os.path.getsize(self.dst) != 0:
                self.data = pickle.load(rf)
            else:
                print("数据库是空的!")

    def create(self, args):  # 创建
        print("Basice Write Func!")
        with open(self.dst, "wb") as wf:
            pickle.dump(self.data, wf)

    def account_auth(self, *args):  # 账户检测
        pass


# 针对db/admin_db/admin_account文件里的管理员信息


class AdminDataControl(DataControl):

    def __init__(self, args):
        print("AdminDataControl")
        print(self)
        super(AdminDataControl, self).__init__(args)

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
        print("UserDataControl")
        print(self)
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
        return os.path.exists(self.dst)  # 用户是否存在

    def create(self, args):
        """

        :param args: args表示传入的要创建的人员信息
        :return:
        """
        with open(self.dst, "wb") as wf:
            if self.user_data is None:
                pickle.dump(args, wf)
            else:
                pickle.dump(self.user_data, wf)

    def read(self):
        with open(self.dst, "rb") as rf:
            if os.path.getsize(self.dst) != 0:
                self.user_data = pickle.load(rf)

    def get_usr_data(self):
        return self.user_data

    def set_usr_data(self, args):
        self.user_data = args

# 以下针对db/course_choosing_sys_db/目录下的数据信息


class SchoolDataControl(DataControl):  # 学校数据类

    def __init__(self, args):
        print("SchoolDataControl")
        print(self)
        super(SchoolDataControl, self).__init__(args)


class ClassDataControl(DataControl):  # 班级数据类

    def __init__(self, args):
        print("ClassDataControl")
        print(self)
        super(ClassDataControl, self).__init__(args)


class CourseDataControl(DataControl):  # 课程数据类

    def __init__(self, args):
        print("CourseDataControl")
        print(self)
        super(CourseDataControl, self).__init__(args)


class StudentDataControl(DataControl):  # 学员数据类

    def __init__(self, args):
        print("StudentDataControl")
        print(self)
        super(StudentDataControl, self).__init__(args)


class TeacherDataControl(DataControl):  # 讲师数据类

    def __init__(self, args):
        print("TeacherDataControl")
        print(self)
        super(TeacherDataControl, self).__init__(args)


