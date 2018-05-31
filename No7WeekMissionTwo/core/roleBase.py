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
        student_list = []  # 保存学员对象

        while True:
            class_name = input("请输入要创建的班级名称(输入 Q 退出):").strip()
            if class_name == 'Q':
                return
            class_info = self.db_handle.search(2)
            print(class_info)
            if class_name in class_info:
                print("\033[35;1m班级存在\033[0m")
                return
            else:
                teacher_name = input("请输入讲师姓名(输入 Q 退出):").strip()
                if teacher_name == 'Q':
                    break
                teacher_info = self.db_handle.search(3)
                if teacher_name in teacher_info:
                    cx = TablesInit.Class(name=class_name, teacher_id=teacher_info.id)
                    class_list.append(cx)
                    while True:
                        import_now = input("是否导入学员? Y/N: ").strip()
                        if import_now == 'Y':
                            class_choice = input("请选择导入班级:").strip()
                            if class_choice in class_info:
                                student_info = self.db_handle.search(1)
                                if len(student_info) == 0:
                                    print("\033[31;1m还没有任何学员可供导入!\033[0m")
                                else:
                                    while True:
                                        student_qq = input("请输入学员QQ号进行导入(Q退出):")
                                        if student_qq == 'Q':
                                            break
                                        result = self.db_handle.search_condition(1, qq=student_qq)
                                        if result is not None:
                                            student_list.append(result)
                                        else:
                                            print("\033[31;1m导入失败,没有这个学员\033[0m")
                                    cx.students = student_list
                            else:
                                print("选择不正确")
                        else:
                            break
                else:
                    print("\033[31;1m没有讲师可以导入!\033[0m")

        print("\033[31;1m创建...\033[0m")
        print("\033[33;1m创建完成\033[0m")
        print("\033[35;1m创建失败\033[0m")
        self.db_handle.add(2, cl=class_list, sl=student_list)

    def create_class_records(self):
        """创建上课记录"""
        print("创建上课记录")

    def modify_class_records(self):
        """修改上课记录"""
        print("修改上课记录")

    def delete_class_records(self):
        """删除上课记录"""
        print("删除上课记录")
