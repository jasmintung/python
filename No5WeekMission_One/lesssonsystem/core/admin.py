# -*-coding=utf-8-*-
__author__ = 'zhangtong'
'''
Contact: puzexiong@163.com
'''
# 管理员类

from core.school import SchoolModule
from core.course import CourseModule
from core.classes import ClassModule
from core.student import StudentModule
from core.teacher import TeacherModule
from core.auth import login_deco
from core.auth import AuthModule
# 管理员数据结构
dict1 = {"0001": "admin1", "0002": "admin2", "0003": "admin3"}


class AdminModule(object):
    def __int__(self):
        self.school_name = None

    @login_deco(8)
    def auth(self):
        # 登陆
        instance_am = AuthModule(0)
        return instance_am.login()

    def create_school(self):  # OK
        # 创建学校
        school_name = input("输入学校名称:")
        t_school = SchoolModule(school_name)
        result = check_interface(t_school)
        if result is False:
            t_school.add_school(school_name)
            self.school_name = school_name
        else:
            pass
        return result

    def create_class(self):  # OK
        # 创建班级
        if self.create_school() is True:  # 学校存在
            class_name = input("输入班级的名称:")
            t_class = ClassModule(self.school_name)
            dict_class = {}
            if check_interface(t_class, self.school_name, class_name) is False:  # 班级不存在, 允许创建
                student_list = []
                while True:
                    print("请输入%s的学员 输入 'Q' 结束" % class_name)
                    student = input()
                    student_list.append(student)
                    if student == 'Q':
                        break
                course_list = []
                while True:
                    print("请输入%s的课程 输入 'Q' 结束" % class_name)
                    course = input()
                    course_list.append(course)
                    if course == 'Q':
                        break
                teacher_list = []
                while True:
                    print("请输入%s的讲师 输入 'Q' 结束" % class_name)
                    teacher = input()
                    teacher_list.append(teacher)
                    if teacher == 'Q':
                        break
                dict_class["学员"] = student_list
                dict_class["课程"] = course_list
                dict_class["讲师"] = teacher_list
                t_class.add_class(class_name, dict_class)
            else:
                print("班级已经存在了!")
        else:
            print("学校不存在!")

    def create_teacher(self):
        # 创建讲师
        if self.create_school() is True:  # 学校存在
            t_teacher = TeacherModule(self.school_name)
            class_list_info = {}
            while True:
                class_list = []
                teacher_name = input("请输入讲师名称:")
                if check_interface(t_teacher, teacher_name) is False:
                    class_name = input("请输入班级名称:")
                    class_list.append(class_name)
                    class_list_info[teacher_name] = class_list
                    if teacher_name == 'Q':
                        break
            else:
                pass
            t_teacher.add_teacher(teacher_name, class_list_info)
        else:
            pass

    def create_course(self):
        # 创建课程
        if self.create_school() is True:  # 学校存在
            t_course = CourseModule(self.school_name)

            currnet_course_length = t_course.get_current_course_list()  # 作为后续增加课程时课程编号计数的基数
            id = currnet_course_length + 1
            dict_course = {}
            dict_school_course = {}
            while True:
                course_id = str(id).rjust(6, "0")
                course_name = input("输入课程名称:")
                if check_interface(t_course, course_name) is False:
                    course_cycle = input("输入课程周期")
                    course_price = input("输入课程价格")
                    dict_course[course_id] = {course_name, course_cycle, course_price}
                    next_opreation = input("继续增加课程回车,否则输入'#'退出")
                    id += 1
                    if next_opreation == '#':
                        dict_school_course[self.school_name] = dict_course
                        t_course.add_course(dict_school_course)
                        break
                else:
                    break

    def create_student(self):
        # 创建学员
        dict_student = {}
        school_name = input("请输入要操作的学校的名称:")
        class_name = input("请输入要操作的班级名称:")
        t_school = SchoolModule(school_name)
        if check_interface(t_school) is True:  # 学校存在
            t_class = ClassModule(school_name)
            if check_interface(t_class) is True:  # 班级存在
                t_student = StudentModule(school_name, class_name)
                id = 1  # 判断已有ID号
                dict_student_name = {}
                while True:
                    list_student_name = []
                    student_name = input("请输入学员姓名:")
                    if check_interface(t_student, student_name) is False:
                        # {"大连": {"0001": ["Jack", "一班"], "0002": ["李老大", "二班"]}}
                        student_id = str(id).rstrip(6, "0")
                        list_student_name.append(student_name)
                        list_student_name.append(class_name)
                        dict_student_name[student_id] = list_student_name
                        next_opreation = input("继续增加课程回车,否则输入'#'退出")
                        id += 1
                        if next_opreation == '#':
                            dict_student[school_name] = dict_student_name
                            t_student.add_student(dict_student)
                            break


def check_interface(obj, *args):  # 将不同类别的值重复检查操作做成接口,方便后期维护
    return obj.check_exists(args)
