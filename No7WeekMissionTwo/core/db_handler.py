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
        result = None
        if type == 0:  # 学员表插入
            result = TablesInit.Student(name=kwargs.get('name'), password=kwargs.get('password'), qq_number=kwargs.get('qq'))
            self.db.add(result)
        elif type == 1:  # 讲师表插入
            result = TablesInit.Teacher(name=kwargs.get('name'), password=kwargs.get('password'))
            self.db.add(result)
        elif type == 2:  # 创建班级
            self.db.add_all(kwargs.get('cl') + kwargs.get('sl'))
            pass
        elif type == 3:  # 创建上课记录
            pass
        elif type == 5:  # 提交作业
            pass
        try:
            self.db.commit()
            return result
        except Exception as ex:
            print(ex)
            self.db.rollback()

    def delete(self):
        pass

    def search(self, type, **kwargs):
        result = None
        if type == 0:  # 查询成绩
            pass
        elif type == 1:  # 查询学员表信息
            result = self.db.query(TablesInit.Student).all()
        elif type == 2:  # 查询班级表信息
            result = self.db.query(TablesInit.Class).all()
        elif type == 3:  # 查询讲师表信息
            result = self.db.query(TablesInit.Teacher).all()
        try:
            self.db.commit()
            return result
        except Exception as ex:
            print(ex)
            self.db.rollback()

    def search_condition(self, type, **kwargs):
        """
        条件搜索
        :param type:
        :param kwargs:
        :return:
        """
        result = None
        if type == 0:  # 查询成绩
            pass
        elif type == 1:  # 查询学员表信息,根据QQ号
            result = self.db.query(TablesInit.Student).filter_by(qq_number=kwargs.get('qq')).first()
        elif type == 2:  # 查询班级表信息
            result = self.db.query(TablesInit.Class).all()
        elif type == 3:  # 查询讲师表信息
            result = self.db.query(TablesInit.Teacher).all()
        try:
            self.db.commit()
            return result
        except Exception as ex:
            print(ex)
            self.db.rollback()

    def modify(self):
        if type == 0:  # 修改上课记录
            pass
        try:
            self.db.commit()
        except Exception as ex:
            print(ex)
            self.db.rollback()