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
        chose_class_list = []

        class_info = self.db_handle.search(2)
        teacher_info = self.db_handle.search(3, name=self.name)
        if teacher_info is not None:
            if class_info is not None:
                # print("id=class_info.teacher_id: ", class_info.teacher_id)
                for cl_info in class_info:
                    if cl_info.teacher_id == teacher_info.id:
                        print(cl_info.name)
                        chose_class_list.append(cl_info.name)
                cl_name = input("请选择要创建上课记录的班级:").strip()
                if cl_name in chose_class_list:
                    print("可以创建上课记录")
                    result = self.db_handle.search(4, t_id=teacher_info.id, c_id=cl_info.id)
                    if result is None:
                        pass
    def modify_class_records(self):
        """修改上课记录"""
        print("修改上课记录")


    def delete_class_records(self):
        """删除上课记录"""
        print("删除上课记录")
