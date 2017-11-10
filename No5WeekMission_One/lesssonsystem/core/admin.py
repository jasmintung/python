# -*-coding=utf-8-*-
__author__ = 'zhangtong'
'''
Contact: puzexiong@163.com
'''
# 管理员类

from core.db_handler import TeacherDataControl
from core.db_handler import ClassDataControl
from core.db_handler import SchoolDataControl
from core.db_handler import StudentDataControl
from core.db_handler import CourseDataControl
from core.auth import login_deco
from core.auth import AuthModule
# 管理员数据结构
dict1 = {"0001": "admin1", "0002": "admin2", "0003": "admin3"}


class AdminModule(object):
    def __int__(self):
        self.school_name = None

    school_id = 1

    @login_deco(8)
    def auth(self):
        # 登陆
        instance_am = AuthModule(0)
        return instance_am.login()

    def func_control(self, args):
        func_dict = {1: self.create_school, 2: self.create_class, 3: self.create_student, 4: self.create_course}
        if args in func_dict:
            func_dict[args]()
        else:
            print("\033[33;1m选择错误!\033[0m")

    def control_operation(self, name):
        self.name = name
        operation_info = """
                请选择:
                1. 创建学校
                2. 创建班级
                3. 创建讲师
                4. 创建课程
                """
        print(operation_info)
        input_operation = int(input().strip(">>"))
        self.func_control(input_operation)

    def create_school(self):  # OK
        # 创建学校
        school_name = input("输入学校名称:")
        instance_t_school = SchoolDataControl()
        instance_t_school.read()
        is_enable = True
        for school_id in instance_t_school.school_data:
            if school_name == instance_t_school.school_data[school_id]:
                print("不能重复创建")
                is_enable = False
                break
        if is_enable is True:
            AdminModule.school_id += 1
            instance_t_school.school_data[AdminModule.school_id] = school_name
            instance_t_school.create()

    def create_class(self):  # OK
        # 创建班级
        school_name = input("输入学校名称:")
        instance_t_school = SchoolDataControl()
        instance_t_school.read()
        is_enable = False
        for school_id in instance_t_school.school_data:
            if school_name == instance_t_school.school_data[school_id]:
                is_enable = True
                break
        if is_enable is True:
            dict_class = {}
            class_name = input("输入要创建或修改的班级名称")
            course_list = []
            while True:
                print("请输入要添加到%s的课程,可一次添加多门课程 输入 'Q' 结束" % class_name)
                course = input()
                course_list.append(course)
                if course == 'Q':
                    break
            teacher_list = []
            while True:
                print("请输入要添加到%s的讲师,可一次添加多名讲师 输入 'Q' 结束" % class_name)
                teacher = input()
                teacher_list.append(teacher)
                if teacher == 'Q':
                    break
            instance_t_class = ClassDataControl()
            instance_t_class.read()
            #  相同的合并,不相同的累加
            if school_name in instance_t_class.class_data.keys():  # 该校区已经创建过班级
                dict_class[school_name][class_name]["课程"] = \
                    instance_t_class.class_data[school_name][class_name]["课程"] + course_list

                instance_t_class.class_data[school_name][class_name]["课程"] = \
                    list(set(dict_class[school_name][class_name]["课程"]))

                dict_class[school_name][class_name]["讲师"] = \
                    instance_t_class.class_data[school_name][class_name]["讲师"] + teacher_list

                instance_t_class.class_data[school_name][class_name]["讲师"] = \
                    list(set(dict_class[school_name][class_name]["讲师"]))
            else:
                instance_t_class.class_data[school_name][class_name]["讲师"] = teacher_list
                instance_t_class.class_data[school_name][class_name]["课程"] = course_list
            instance_t_class.create()
        else:
            print("\033[33;1m学校不存在,无法创建班级!\033[0m")

    def create_teacher(self):
        # 创建讲师
        school_name = input("输入学校名称:")
        instance_t_school = SchoolDataControl()
        instance_t_school.read()
        is_enable = False
        for school_id in instance_t_school.school_data:
            if school_name == instance_t_school.school_data[school_id]:
                is_enable = True
                break
        if is_enable is True:
            dict_teacher = {}
            while True:
                teacher_list = []
                teacher_name = input("请输入讲师名称:")
                teacher_list.append(teacher_name)
                if teacher_name == 'Q':
                    break
            instance_t_teacher = TeacherDataControl()
            instance_t_teacher.read()
            if school_name in instance_t_teacher.teacher_data.keys():  # 该校区已经创建过讲师
                dict_teacher[school_name] = instance_t_teacher.teacher_data[school_name] + teacher_list
                instance_t_teacher.teacher_data[school_name] = dict_teacher[school_name]
            else:
                instance_t_teacher.teacher_data[school_name] = teacher_list

            instance_t_teacher.create()

    def create_course(self):
        # 创建课程

        instance_t_school = SchoolDataControl()
        instance_t_school.read()
        is_enable = False
        print(instance_t_school.school_data)
        school_name = input("输入学校名称:")
        for school_id in instance_t_school.school_data:
            if school_name == instance_t_school.school_data[school_id]:
                is_enable = True
                break
        if is_enable is True:
            instance_t_course = CourseDataControl()
            instance_t_course.read()
            current_course_id = instance_t_course.course_id  # 作为后续增加课程时课程编号计数的基数
            dict_course = {}
            dict_school_course = {}
            while True:
                course_id = str(current_course_id).rjust(6, "0")
                course_name = input("输入课程名称:")
                course_cycle = input("输入课程周期")
                course_price = input("输入课程价格")
                dict_course[course_id].append(course_name)
                dict_course[course_id].append(course_cycle)
                dict_course[course_id].append(course_price)
                next_operation = input("继续增加课程回车,否则输入'Q'退出")
                if next_operation == "Q":
                    break
                current_course_id += 1
            if school_name in instance_t_course.course_data.keys():  # 该校区已经创建过课程
                dict_school_course.update(instance_t_course.course_data[school_name])
                dict_school_course.update(dict_course)
                instance_t_course.course_data[school_name] = dict_school_course
            else:
                instance_t_course.course_data[school_name] = dict_course
        else:
            print("\033[31;1m学校不存在!\033[0m")
    # def create_student(self):
    #     # 创建学员
    #     dict_student = {}
    #     school_name = input("请输入要操作的学校的名称:")
    #     class_name = input("请输入要操作的班级名称:")
    #     t_school = SchoolModule(school_name)
    #     if check_interface(t_school) is True:  # 学校存在
    #         t_class = ClassModule(school_name)
    #         if check_interface(t_class) is True:  # 班级存在
    #             t_student = StudentModule(school_name, class_name)
    #             id = 1  # 判断已有ID号
    #             dict_student_name = {}
    #             while True:
    #                 list_student_name = []
    #                 student_name = input("请输入学员姓名:")
    #                 if check_interface(t_student, student_name) is False:
    #                     # {"大连": {"0001": ["Jack", "一班"], "0002": ["李老大", "二班"]}}
    #                     student_id = str(id).rstrip(6, "0")
    #                     list_student_name.append(student_name)
    #                     list_student_name.append(class_name)
    #                     dict_student_name[student_id] = list_student_name
    #                     next_opreation = input("继续增加课程回车,否则输入'#'退出")
    #                     id += 1
    #                     if next_opreation == '#':
    #                         dict_student[school_name] = dict_student_name
    #                         t_student.add_student(dict_student)
    #                         break


def check_interface(obj, *args):  # 将不同类别的值重复检查操作做成接口,方便后期维护
    return obj.check_exists(args)
