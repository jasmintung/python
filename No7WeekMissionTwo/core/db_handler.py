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
        result_t = self.db.query(TablesInit.Teacher).filter_by(name=self.name, password=self.password).all()
        if len(result_t) > 0:
            return T_PASS, result_t
        result_s = self.db.query(TablesInit.Student).filter_by(name=self.name, password=self.password).all()
        if len(result_s) > 0:
            return S_PASS, result_s
        return NO_PASS, None

    def add(self):
        pass

    def delete(self):
        pass

    def search(self):
        pass

    def modify(self):
        pass
