import os
import pickle
from conf import settings
file_dst = settings.FILE_BASE


class DataControl(object):

    def __init__(self):
        pass

    def create(self, *args):  # 创建
        pass

    def read(self):  # 读取
        pass

    def update(self):  # 更新
        pass

    def account_auth(self, *args):  # 账户检测
        pass


class AdminDataControl(DataControl):

    def __init__(self):
        super(AdminDataControl, self).__init__()

    def create(self):
        pass

    def account_auth(self, *args):
        """

        :param args: 0: 用户名,1: 密码
        :return: 登陆是否成功表示True: 登陆成功, False: 登陆失败
        """
        login_statue = False
        admin_db_dst = "%s/%s/%s" % (file_dst["path"], file_dst["dir_name1"], file_dst["admin_file_name"])
        if os.path.exists(admin_db_dst) is True:
            with open(admin_db_dst, "r", encoding="utf-8") as rf:
                admin_account_data = pickle.load(rf)
                print(admin_account_data)
                for i in admin_account_data:
                    if args[0] in admin_account_data[i] and args[1] in admin_account_data[i]:
                        print("登陆成功!")
                        login_statue = True
        else:
            print("文件不存在!")
        return login_statue


class UserDataControl(DataControl):

    def __init__(self):
        super(UserDataControl, self).__init__()

    def account_auth(self, *args):
        """

        :param args: 0: 用户类型（1:学生、2:讲师）1: 用户名,2: 密码
        :return: 登陆是否成功表示True: 登陆成功, False: 登陆失败
        """
        login_statue = False
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
                    login_statue = True
        else:
            print("不存在这个用户请注册!")
        return login_statue

    def create(self, *args):
        pass


class TeacherDataControl(DataControl):

    def __init__(self):
        super(TeacherDataControl, self).__init__()

    ccsys_teacher_dst = "%s/%s/%s" % (file_dst["path"], file_dst["dir_name2"], file_dst["teacher_file_name"])

    def create(self, *args):
        """

        :param args: 0: 学校, 1: 讲师
        :return: 创建结果
        """

        teacher_data = self.read(1)
        print(teacher_data)
        with open(TeacherDataControl.ccsys_teacher_dst, "w", encoding="utf-8") as wf:
            teacher_data[args[0]].append(args[1])
            pickle.dump(teacher_data, wf)

    def read(self, *args):
        """

        :param args: 目前 : args0: 学校, args1: 0 or 1
        :return: 0: 返回讲师列表, 1 返回整个文件内容)
        """

        if os.path.exists(TeacherDataControl.ccsys_teacher_dst) is True:
            with open(TeacherDataControl.ccsys_teacher_dst, "r", encoding="utf-8") as rf:
                teacher_data = pickle.load(rf)
                print(teacher_data)
                if args[1] == 0:
                    return teacher_data[args[0]]
                elif args[1] == 1:
                    return teacher_data


class SchoolDataControl(DataControl):

    def __init__(self):
        super(SchoolDataControl, self).__init__()

    ccsys_school_dst = "%s/%s/%s" % (file_dst["path"], file_dst["dir_name2"], file_dst["school_file_name"])

    def create(self, *args):
        """

        :param args: args0: key,  args1: value
        :return: 创建结果
        """
        school_data = self.read()
        print(school_data)
        with open(SchoolDataControl.ccsys_school_dst, "w", encoding="uft-8") as wf:
            school_data[args[0]] = args[1]
            pickle.dump(school_data, wf)

    def read(self, *args):
        """

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

    ccsys_class_dst = "%s/%s/%s" % (file_dst["path"], file_dst["dir_name2"], file_dst["class_file_name"])

    def create(self, *args):
        """

        :param args: 选课数据库班级表
        :return:
        """
        with open(ClassDataControl.ccsys_class_dst, "w", encoding="utf-8") as wf:
            pickle.dump(args, wf)

    def read(self, *args):
        """
        获取班级列表
        :param args: args0: 学校, args1: 0 or 1
        :return: 0: 班级列表, 1 整个文件内容
        """
        with open(ClassDataControl.ccsys_class_dst, "r", encoding="utf-8") as rf:
            class_data = pickle.load(rf)
            print(class_data)
            if args[0] == 0:
                return class_data[args[0]]
            elif args[0] == 1:
                return class_data


class CourseDataControl(DataControl):

    def __init__(self):
        super(CourseDataControl, self).__init__()

    def create(self, *args):
        pass

    def read(self, *args):
        pass


class StudentDataControl(DataControl):

    def __init__(self):
        super(StudentDataControl, self).__init__()

    def create(self):
        pass

    def read(self, *args):
        pass
