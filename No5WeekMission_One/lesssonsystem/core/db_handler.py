import os
import pickle
import copy
from conf import settings
file_dst = settings.FILE_BASE


class DataControl(object):

    def __init__(self, dst):
        self.dst = dst
        self.write_file_data = None

    def create(self):  # 创建
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
# 针对db/admin_db目录下的管理员信息


class AdminDataControl(DataControl):

    def __init__(self):
        super(AdminDataControl, self).__init__()

    def create(self):
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
                admin_account_data = pickle.load(rf)
                print(admin_account_data)
                for i in admin_account_data:
                    if args[0] in admin_account_data[i] and args[1] in admin_account_data[i]:
                        login_statue = 0
        else:
            print("文件不存在!")
        return login_statue

# 针对db/user_db/目录下的学生,讲师注册信息


class UserDataControl(DataControl):

    def __init__(self, dst):
        self.dst = dst
        super(UserDataControl, self).__init__(dst)

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
            with open(user_db_dst, "r", encoding="utf-8") as rf:
                user_data = pickle.load(rf)
                print(user_data)
                if user_data["name"] == args[1] and user_data["password"] == args[2]:
                    login_statue = 0  # 账户匹配
                elif user_data["name"] == args[1] and user_data["password"] != args[2]:
                    login_statue = 1  # 密码不对
        else:
            login_statue = 2  # 账户不存在
        return login_statue

    def create(self):
        pass

    def read(self):
        with open(self.dst, "r", encoding="utf-8") as rf:
            user_dict = pickle.load(rf)
            return user_dict

# 以下针对db/course_choosing_sys_db/目录下的数据信息


class TeacherDataControl(DataControl):

    def __init__(self):
        super(TeacherDataControl, self).__init__()
        self.teacher_data = None

    ccsys_teacher_dst = "%s/%s/%s" % (file_dst["path"], file_dst["dir_name2"], file_dst["teacher_file_name"])

    def create(self, *args):
        """
        创建讲师
        :param args: 0: 学校, 1: 讲师
        :return: 创建结果
        """
        with open(self.dst, "w", encoding="utf-8") as wf:
            pickle.dump(self.teacher_data, wf)

    def read(self):
        """
        获取讲师整个文件内容)
        """
        if os.path.exists(TeacherDataControl.ccsys_teacher_dst) is True:
            with open(TeacherDataControl.ccsys_teacher_dst, "r", encoding="utf-8") as rf:
                self.teacher_data = pickle.load(rf)
                print(self.teacher_data)


class SchoolDataControl(DataControl):

    def __init__(self, args):
        super(SchoolDataControl, self).__init__()
        self.school_data = None
        self.dst = args
    ccsys_school_dst = "%s/%s/%s" % (file_dst["path"], file_dst["dir_name2"], file_dst["school_file_name"])

    def create(self):
        """
        创建学校
        :return: 创建结果
        """
        with open(SchoolDataControl.ccsys_school_dst, "w", encoding="uft-8") as wf:
            pickle.dump(self.school_data, wf)

    def read(self):
        """
        获取学校列表
        :param args:
        :return: 学校列表
        """

        if os.path.exists(SchoolDataControl.ccsys_school_dst) is True:
            with open(SchoolDataControl.ccsys_school_dst, "r", encoding="utf-8") as rf:
                school_data = pickle.load(rf)
                print(school_data)
                return school_data


class ClassDataControl(DataControl):

    def __init__(self):
        super(ClassDataControl, self).__init__()
        self.class_data = None
        self.write_file_data = None
    ccsys_class_dst = "%s/%s/%s" % (file_dst["path"], file_dst["dir_name2"], file_dst["class_file_name"])

    def create(self):
        """
        创建班
        :return:
        """
        with open(ClassDataControl.ccsys_class_dst, "w", encoding="utf-8") as wf:
            pickle.dump(self.class_data, wf)

    def read(self):
        """
        获取班级文件
        """
        with open(ClassDataControl.ccsys_class_dst, "r", encoding="utf-8") as rf:
            self.class_data = pickle.load(rf)
            print(self.class_data)

    def merge_dicts(self, *args):
        """

        :param x: 要合并的字典
        :return:
        """
        self.class_data[args[0]][args[1]][args[2]].append(args[3])
        self.write_file_data = self.class_data


class CourseDataControl(DataControl):

    def __init__(self, args):
        super(CourseDataControl, self).__init__(args)
        self.course_data = None
        self.dst = args
    ccsys_course_dst = "%s/%s/%s" % (file_dst["path"], file_dst["dir_name2"], file_dst["course_file_name"])

    def create(self):
        """
        创建课程
        :return:
        """
        with open(self.dst, "w", encoding="utf-8") as wf:
            pickle.dump(self.course_data, wf)

    def read(self):
        """
        获取课程列表
        :param args: args0: 学校, args1: 0 or 1
        :return:0: 课程列表, 1 整个文件内容
        """
        with open(CourseDataControl.ccsys_course_dst, "r", encoding="utf-8") as rf:
            self.course_data = pickle.load(rf)
            print(self.course_data)


class StudentDataControl(DataControl):

    def __init__(self):
        super(StudentDataControl, self).__init__()
        self.student_data = None
        self.school_name = None
        self.write_file_data = None

    ccsys_student_dst = "%s/%s/%s" % (file_dst["path"], file_dst["dir_name2"], file_dst["student_file_name"])

    def create(self, *args):
        """
        创建学生
        :param args:文件地址
        :return:
        """
        with open(StudentDataControl.ccsys_student_dst, "w", encoding="utf-8") as wf:
            pickle.dump(self.write_file_data, wf)

    def merge_dicts(self, x):
        """

        :param x: 要合并的字典
        :return:
        """
        z = copy.deepcopy(self.student_data)
        z[self.school_name].update(x[self.school_name])
        self.write_file_data = z

    def read(self):
        """
        获取整个文件内容
        """
        with open(StudentDataControl.ccsys_student_dst, "r", encoding="utf-8") as rf:
            self.student_data = pickle.load(rf)
            print(self.student_data)
