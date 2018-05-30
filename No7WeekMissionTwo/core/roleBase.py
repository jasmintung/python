


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

    def create_class_records(self):
        """创建上课记录"""
        print("创建上课记录")

    def modify_class_records(self):
        """修改上课记录"""
        print("修改上课记录")

    def delete_class_records(self):
        """删除上课记录"""
        print("删除上课记录")
