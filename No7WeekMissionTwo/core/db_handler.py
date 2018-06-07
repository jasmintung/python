from db import TablesInit
from sqlalchemy import func
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
            for Class in cl:
                print("class obj:", Class)
            for Student in sl:
                print("student obj:", Student)
            if len(cl) == 0 and len(sl) == 0:
                print("没有数据不用操作数据库")
                return
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
            if kwargs.get('class_rc') is not None:
                self.db.add(kwargs.get('class_rc'))
            if kwargs.get('students_rc') is not None:
                self.db.add_all(kwargs.get('students_rc'))
        elif type == 5:  # 提交作业
            result = TablesInit.MissionRecords(name=kwargs.get('name'), statue=kwargs.get('statue'),
                                               class_record_id=kwargs.get('class_rc_id'))
            self.db.add(result)
        try:
            self.db.commit()
            print("\033[33;1m创建完成\033[0m")
            return result
        except Exception as ex:
            print(ex)
            self.db.rollback()
            print("\033[35;1m创建失败\033[0m")

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
                print(kwargs)
                if len(kwargs) == 0:
                    result = self.db.query(TablesInit.Class).all()
                    print("1111:", result)
                    # result = self.db.query(TablesInit.Teacher).filter_by(id=result.teacher_id).first()
                else:
                    print("2222:", result)
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
            elif type == 4:  # 查询上课记录表返回记录总数
                cl_count = self.db.query(func.count('*')).filter(TablesInit.ClassRecords.class_id
                                                                 == kwargs.get('c_id')).scalar()
                print("cl_count: ", cl_count)
                result = self.db.query(TablesInit.ClassRecords).filter_by(course_id=cl_count+1,
                                                                          teacher_id=kwargs.get('t_id'),
                                                                          class_id=kwargs.get('c_id')).first()
                if result is None:
                    print("记录数:", cl_count)
                    return int(cl_count + 1)
                else:
                    return 0
            elif type == 5:  # 查询上课记录表中的学员QQ号
                qq_list = []
                ret = self.db.query(TablesInit.StudentRecords.qq_number).all()  # 返回的是元组对象
                # print
                for qq in ret:
                    qq_list.append(qq[0])
                result = set(qq_list)
                # query4.count()
                # print
                # session.query(func.count('*')).select_from(User).scalar()
                # print
                # session.query(func.count('1')).select_from(User).scalar()
                # print
                # session.query(func.count(User.id)).scalar()
                # print
                # session.query(func.count('*')).filter(User.id > 0).scalar()  # filter() 中包含 User，因此不需要指定表
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
                # self.db.commit
            elif type == 4:  # 根据讲师ID,班级名称查询
                result = self.db.query(TablesInit.Class).filter_by(name=kwargs.get('cl_name'),
                                                                   teacher_id=kwargs.get('tc_id')).all()
            elif type == 5:  # 根据QQ号去查询学员参加的班级
                result = self.db.query(TablesInit.Student).filter_by(qq_number=kwargs.get('qq')).all()
            elif type == 6:  # 根据QQ号去查询学员记录
                # 获得学员上课记录表中的class record id
                course_id = {}
                result_st = self.db.query(TablesInit.StudentRecords).filter(
                    TablesInit.StudentRecords.qq_number == kwargs.get('qq')).filter(TablesInit.StudentRecords.statue == 0).all()
                for class_rc_id in result_st:
                    result_st = self.db.query(TablesInit.ClassRecords).filter_by(id=class_rc_id.class_record_id).first()
                    if kwargs.get('cl_id') == result_st.class_id:
                        mission_rc = self.db.query(TablesInit.MissionRecords).filter_by(name=kwargs.get('st_name'),
                                                                                        class_record_id=result_st.id).first()  # 作业提交表里看是否已经提交了作业
                        if mission_rc is not None:
                            if mission_rc.statue == 0:  # 没有提交
                                course_id[result_st.id] = result_st.course_id  # 符合条件的班级的那节课id
                        else:
                            course_id[result_st.id] = result_st.course_id  # 符合条件的班级的那节课id
                result = course_id
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