from db import TablesInit


class Role(object):
    def __init__(self, db_handle, name, password):
        self.db_handle = db_handle
        self.name = name
        self.password = password

    def search_records(self):
        """查看记录成绩等信息"""
        pass

    def enroll(self):
        """
        用户注册
        :return:
        """
        pass


class Student(Role):
    def __init__(self, db_handle, name, password, qq):
        super(Student, self).__init__(db_handle, name, password)
        self.qq = qq

    def enroll(self):
        """
        学员注册
        :return:
        """
        self.db_handle.add(0, name=self.name, password=self.password, qq=self.qq)

    def commit_mission(self):
        """提交作业"""
        print("提交作业")
        course_id_list = []
        result = self.db_handle.search_condition(5, qq=self.qq)

        cl_name_list = (cl_name for index in result for cl_name in index.Class)
        print("请选择班级:")
        for index in result:
            for cl_name in index.Class:
                print("|%s" % cl_name.name, end=' ')
        print(">>".strip(), end=' ')
        class_name = input().strip()
        for x in cl_name_list:
            if class_name == x.name:
                result = self.db_handle.search_condition(6, qq=self.qq, cl_id=x.id, cl_name=x.name)  # 将班级ID,学员QQ传递下去
                # for cl_id in result:
                #     print("对应的上课记录表ID: ", cl_id.class_record_id)
                #     rc = self.db_handle.search_condition(7, cl_id=cl_id.class_record_id, cl_name=x.name)
                #     print("第%d节课" % rc.course_id)
                #     course_id_list.append(rc.course_id)
        class_index = input("提交哪节课的作业:").strip()
        if class_index in course_id_list:
            print("ok")

    def view_score(self):
        """查看成绩"""
        print("查看成绩")


class Teacher(Role):
    def __init__(self, db_handle, name, password):
        super(Teacher, self).__init__(db_handle, name, password)

    def enroll(self):
        """
        讲师注册
        :return:
        """
        self.db_handle.add(1, name=self.name, password=self.password)

    def create_classes(self):
        """创建班级"""
        print("创建班级")
        class_list = []  # 保存班级对象
        class_exists = False
        while True:
            student_list = []  # 保存学员对象
            class_name = input("请输入要创建的班级名称(输入 Q 退出):").strip()
            if class_name == 'Q':
                break
            class_info = self.db_handle.search(2, name=class_name)
            teacher_info = self.db_handle.search(3, name=self.name)
            if teacher_info is not None:
                if class_info is not None:
                    # print("id=class_info.teacher_id: ", class_info.teacher_id)
                    if class_info.teacher_id != teacher_info.id:
                        print("\033[34;1m班级已指定其它讲师,无法创建\033[0m")
                        continue
                    class_exists = True
                    print("\033[35;1m班级已经存在,当前可进行更新修改\033[0m")
                else:
                    print("\033[35;1m新增班级\033[0m")
                if not class_exists:
                    class_info = TablesInit.Class(name=class_name, teacher_id=teacher_info.id)
                    # class_list.append(class_info)
                else:
                    pass
                while True:
                    import_now = input("是否导入新学员? Y/N: ").strip()
                    if import_now == 'Y':
                        student_info = self.db_handle.search(1)
                        if student_info is None:
                            print("\033[31;1m还没有任何学员可供导入!\033[0m")
                            break
                        else:
                            while True:
                                student_qq = input("请输入学员QQ号进行导入(Q退出):")
                                if student_qq == 'Q':
                                    break
                                result = self.db_handle.search_condition(1, qq=student_qq)

                                if result is not None:
                                    if len(result.Class) == 0:
                                        if result not in student_list:
                                            student_list.append(result)
                                    else:
                                        print("result.Class:", result.Class)
                                        for name in result.Class:
                                            if class_name == name.name:
                                                print("\033[42;1m学员已经在这个班里了\033[0m")
                                            else:
                                                if result not in student_list:
                                                    student_list.append(result)
                                else:
                                    print("\033[31;1m导入失败,没有这个学员\033[0m")
                            class_info.students = student_list
                            if class_info not in class_list:
                                print("插入的class:", class_info)
                                class_list.append(class_info)
                    else:
                        break
                else:
                    pass
            else:
                print("\033[31;1m没有讲师可以导入!\033[0m")
                return
        print("\033[31;1m创建...\033[0m")
        self.db_handle.add(2, cl=class_list, sl=student_list)

    def create_class_records(self):
        """创建上课记录"""
        print("创建上课记录")
        class_rc_instance = None
        student_cl_list = []
        chose_class_list = []

        class_info = self.db_handle.search(2)  # 获取所有班级
        print("class info:", class_info)
        teacher_info = self.db_handle.search(3, name=self.name)  # 获取登陆讲师的信息
        print("teacher info:", teacher_info)
        if teacher_info is not None:
            if class_info is not None:
                # print("id=class_info.teacher_id: ", class_info.teacher_id)
                for cl_info in class_info:
                    if cl_info.teacher_id == teacher_info.id:  # 找到讲师执教的班级
                        print(cl_info.name)
                        chose_class_list.append(cl_info)
                cl_name = input("请选择要创建上课记录的班级:").strip()
                for itc in chose_class_list:
                    if cl_name == itc.name:
                        print("可以创建上课记录")
                        print("teacher id: %d class id: %d" % (teacher_info.id, itc.id))
                        result = self.db_handle.search(4, t_id=teacher_info.id, c_id=itc.id)
                        if result != 0:
                            print(type(result))
                            print(result)
                            class_rc_instance = TablesInit.ClassRecords(course_id=result, teacher_id=teacher_info.id,
                                                                        class_id=itc.id, course_time="2012-08-18")
                            print("上课记录表对象:", class_rc_instance)
                            result_cl = self.db_handle.search_condition(4, cl_name=cl_name, tc_id=teacher_info.id)  # 查找所有符合条件的班级
                            #  根据result去获得对应学员信息
                            print("导入记录的学员有:")
                            for cl_it in result_cl:
                                for stu_info in cl_it.students:
                                    print(stu_info.qq_number)
                                    st_cl_rc = TablesInit.StudentRecords(qq_number=stu_info.qq_number,
                                                                         statue=0, score=0, class_record_id=itc.id)
                                    student_cl_list.append(st_cl_rc)
                            class_rc_instance.children = student_cl_list
                if class_rc_instance is None or len(student_cl_list) == 0:
                    return

                self.db_handle.add(3, class_rc=class_rc_instance, students_rc=student_cl_list)

    def modify_class_records(self):
        """修改上课记录"""
        print("修改上课记录")


    def delete_class_records(self):
        """删除上课记录"""
        print("删除上课记录")
