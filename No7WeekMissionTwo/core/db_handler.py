from db import TablesInit
T_PASS = 1  # 是讲师登陆并通过
S_PASS = 2  # 是学员登陆并通过
NO_PASS = 0  # 登陆不通过


class DBControle(object):
    def __init__(self, db, name, password):
        self.db = db
        self.name = name
        self.password = password

    def verify(self):
        result_t = self.db.query(TablesInit.Teacher).filter_by(name=self.name, password=self.password).first()
        if result_t is not None:
            # print("result_t:", result_t.name)
            return T_PASS, result_t
        result_s = self.db.query(TablesInit.Student).filter_by(name=self.name, password=self.password).first()
        if result_s is not None:
            # print("result_s:", result_s.name, result_s.password)
            return S_PASS, result_s
        return NO_PASS, None

    def add(self, type, **kwargs):
        if type == 0:  # 学员表插入
            student_obj = TablesInit.Student(name=kwargs.get('name'), password=kwargs.get('password'), qq_number=kwargs.get('qq'))
            self.db.add(student_obj)
        elif type == 1:  # 讲师表插入
            teacher_obj = TablesInit.Teacher(name=kwargs.get('name'), password=kwargs.get('password'))
            self.db.add(teacher_obj)
        elif type == 2:
            pass
        elif type == 3:
            pass
        elif type == 4:
            pass
        elif type == 5:
            pass
        try:
            self.db.commit()
        except Exception as ex:
            print(ex)
            self.db.rollback()

    def delete(self):
        pass

    def search(self):
        pass

    def modify(self):
        pass
