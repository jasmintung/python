# -*-coding=utf-8-*-
__author__ = 'zhangtong'
'''
Contact: puzexiong@163.com
'''
from conf import settings
file_dst = settings.FILE_BASE
from core.db_handler import ClassDataControl
from core.course import CourseModule
from core.teacher import TeacherModule

# 班级类
# 选课数据库班级表
# dict1 = {"成都": {"一班": {"课程": ["JAVA", "Android", "Unity3D", "Python"],
#                        "讲师": ["Alex", "Tom"]},
#                 "二班": {"课程": ["C++", "C#", "Go", "Python"],
#                        "讲师": ["Jack", "Jmy"]}},
#          "武汉": {"一班": {"课程": ["算法导论", "软件工程"], "讲师": ["Mobile", "Papa"]}}}


class ClassModule(object):
    def __init__(self, school_name):
        self.school_name = school_name
        self.class_data = {}
    ccsys_class_dst = "%s/%s/%s" % (file_dst["path"], file_dst["dir_name2"], file_dst["class_file_name"])

    def check_exists(self):  # 后面可考虑做成接口
        # 检查要创建的班级是否已经存在dict1
        is_exists = False
        # 数据库查询
        return is_exists

    def get_Class_data(self):
        return self.class_data

    def search_class_data(self):
        instance_cs = ClassDataControl(ClassModule.ccsys_class_dst)
        self.obj = instance_cs
        instance_cs.read()
        self.class_data = instance_cs.get_class_data()

    def add_class(self):  # 增加班级的时候,目前课程，讲师列表必须写入信息,如果还没有能够录入的班级和讲师则提示不能创建班级
        dict_class = {}
        print("输入要在 \"%s\" 创建或修改的 班级 名称" % self.school_name)
        class_name = input()
        course_list = []
        instance_t_course = CourseModule(self.school_name)
        instance_t_course.search_course_data()
        while True:  # 这里要加个判断,判断即将修改或者添加的 课程 有没有在这个校区创建过,没有创建过提示不能添加!
            print("请输入要添加或者修改\"%s\"的课程,回车继续, 输入 'Q' 结束" % class_name)
            course = input()
            if course == 'Q':
                break
            instance_t_course.set_course_name(course)
            if instance_t_course.check_exists() is True:
                course_list.append(course)
            else:
                print("\033[34;1m该课程还未创建,请先通过 \"创建课程\" 功能创建该课程!\033[0m")
        teacher_list = []
        instance_t_teacher = TeacherModule(self.school_name)
        instance_t_teacher.search_teacher_data()

        while True:  # 这里要加个判断,判断即将修改或者添加的 讲师 有没有在这个校区创建过,没有创建过提示不能添加!
            print("请输入要添加或者修改\"%s\"的讲师,回车继续 输入 'Q' 结束" % class_name)
            teacher = input()
            if teacher == 'Q':
                break
            instance_t_teacher.set_teacher_name(teacher)
            if instance_t_teacher.check_exists() is True:
                teacher_list.append(teacher)
            else:
                print("\033[34;1m该讲师还未创建,请先通过 \"创建讲师\" 功能创建该讲师!\033[0m")
        #  相同的合并,不相同的累加
        class_dict = {}
        class_info_dict = {}
        class_info_dict["课程"] = course_list
        class_info_dict["讲师"] = teacher_list
        if self.class_data is None:  # ok
            print("首次创建班级")
            class_dict[class_name] = class_info_dict
            dict_class[self.school_name] = class_dict
            self.obj.set_class_data(dict_class)
        else:
            if self.school_name in self.class_data:  # 班级数据库有这个校区了   ok
                if self.class_data[self.school_name].get(class_name) is None:  # 这个校区还没有要创建的班级
                    self.class_data[self.school_name][class_name] = class_info_dict
                else:  # 这个校区已经存在要创建的班级了,所以实际做更新班级信息处理
                    class_dict[class_name] = class_info_dict
                    dict_class[self.school_name] = class_dict
                    dict_class[self.school_name][class_name]["课程"] = \
                        self.class_data[self.school_name].get(class_name).get("课程") + course_list

                    self.class_data[self.school_name][class_name]["课程"] = \
                        list(set(dict_class[self.school_name][class_name]["课程"]))

                    dict_class[self.school_name][class_name]["讲师"] = \
                        self.class_data[self.school_name].get(class_name).get("讲师") + teacher_list

                    self.class_data[self.school_name][class_name]["讲师"] = \
                        list(set(dict_class[self.school_name][class_name]["讲师"]))
            else:  # ok
                class_dict[class_name] = class_info_dict
                self.class_data[self.school_name] = class_dict
            self.obj.set_class_data(self.class_data)
        self.obj.create(None)
