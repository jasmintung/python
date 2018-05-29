class Role(object):
    def __init__(self, db_handle, name, password):
        self.db_handle = db_handle
        self.name = name
        self.password = password

    def search_records(self):
        """查看记录成绩等信息"""
        pass

    def enroll(self, role_type):
        """
        用户注册
        :return:
        """


class Student(Role):
    def __init__(self, db_handle, name, password, qq):
        super(Student, self).__init__(db_handle, name, password)
        self.qq = qq

    def commit_mission(self):
        """提交作业"""
        pass

    def view_score(self):
        """查看成绩"""
        pass


class Teacher(Role):
    def __init__(self, db_handle, name, password):
        super(Teacher, self).__init__(db_handle, name, password)

    def create_classes(self):
        """创建班级"""
        pass

    def create_class_records(self):
        """创建上课记录"""
        pass

    def modify_class_records(self):
        """修改上课记录"""
        pass

    def delete_class_records(self):
        """删除上课记录"""
        pass