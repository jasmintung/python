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
            cl = kwargs.get('cl')
            sl = kwargs.get('sl')
            print("class obj:", cl)
            print("student obj:", sl)
            if len(cl) == 0 and len(sl) == 0:
                print("没有数据不用操作数据库")
            else:
                if len(cl) == 0 and len(sl) != 0:
                    print("插入S")
                    self.db.add_all(sl)
                elif len(cl) != 0 and len(sl) == 0:
                    print("插入C")
                    self.db.add_all(cl)
                else:
                    self.db.add_all(sl + cl)
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
        try:
            if type == 0:  # 查询成绩
                pass
            elif type == 1:  # 查询学员表信息
                result = self.db.query(TablesInit.Student).all()
            elif type == 2:  # 查询班级表信息
                if kwargs is None:
                    result = self.db.query(TablesInit.Class).all()
                else:
                    for key in kwargs:
                        print(key, kwargs[key])
                        if key == 'name':
                            result = self.db.query(TablesInit.Class).filter_by(name=kwargs[key]).first()
            elif type == 3:  # 查询讲师表信息
                if kwargs is None:
                    result = self.db.query(TablesInit.Teacher).all()
                else:
                    for key in kwargs:
                        print(key, kwargs[key])
                        if key == 'name':
                            result = self.db.query(TablesInit.Teacher).filter_by(name=kwargs[key]).first()
                        elif key == 'id':
                            result = self.db.query(TablesInit.Teacher).filter_by(id=kwargs[key]).first()
                        print(result.name)
                        print(result.id)
                print("查询结果:", result)
                # self.db.commit()
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
        try:
            if type == 0:  # 查询成绩
                pass
            elif type == 1:  # 查询学员表信息,根据QQ号
                result = self.db.query(TablesInit.Student).filter_by(qq_number=kwargs.get('qq')).first()
            elif type == 2:  # 查询班级表信息
                result = self.db.query(TablesInit.Class).all()
            elif type == 3:  # 查询讲师表信息
                result = self.db.query(TablesInit.Teacher).all()
                # self.db.commit()
            return result
        except Exception as ex:
            print(ex)
            self.db.rollback()

    def modify(self, type):
        if type == 0:  # 修改上课记录
            pass
        elif type == 1:  # 修改班级信息
            pass
        try:
            self.db.commit()
        except Exception as ex:
            print(ex)
            self.db.rollback()