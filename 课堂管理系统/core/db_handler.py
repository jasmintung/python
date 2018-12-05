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

    def delete(self, **kwargs):
        try:
            result = self.db.query(TablesInit.ClassRecords).filter_by(id=kwargs.get('id')).first()
            self.db.delete(result)
            self.db.commit()
            print("\033[33;1m删除成功\033[0m")
        except Exception as ex:
            print(ex)
            self.db.rollback()

    def search(self, type, **kwargs):
        result = None
        try:
            if type == 0:  # 查询成绩
                pass
            elif type == 1:  # 查询学员表信息
                result = self.db.query(TablesInit.Student).all()
            elif type == 2:  # 查询班级表信息
                # print(kwargs)
                if len(kwargs) == 0:
                    result = self.db.query(TablesInit.Class).all()
                    # print("1111:", result)
                    # result = self.db.query(TablesInit.Teacher).filter_by(id=result.teacher_id).first()
                else:
                    # print("2222:", result)
                    for key in kwargs:
                        # print(key, kwargs[key])
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
                # print("查询结果:", result)
                # self.db.commit()
            elif type == 4:  # 查询上课记录表返回记录总数
                cl_count = self.db.query(func.count('*')).filter(TablesInit.ClassRecords.class_id
                                                                 == kwargs.get('c_id')).scalar()
                # print("cl_count: ", cl_count)
                result = self.db.query(TablesInit.ClassRecords).filter_by(course_id=cl_count+1,
                                                                          teacher_id=kwargs.get('t_id'),
                                                                          class_id=kwargs.get('c_id')).first()
                if result is None:
                    # print("记录数:", cl_count)
                    return int(cl_count + 1)
                else:
                    return 0
            elif type == 5:  # 查询上课记录表中的学员QQ号
                qq_list = []
                tc_id = self.db.query(TablesInit.Teacher.id).filter_by(name=kwargs.get('tc_name')).first()[0]
                # print("讲师ID:", tc_id)
                ret = self.db.query(TablesInit.ClassRecords).filter_by(teacher_id=tc_id).all()
                # print(ret)
                for stu in ret:
                    for qq in stu.children:
                        qq_list.append(qq.qq_number)
                # cl_id = self.db.query(TablesInit.ClassRecords.id).filter_by(teacher_id=tc_id).all()  # 找到讲师上课记录ID
                #
                # cl_id_list = [x[0] for x in cl_id]
                # print("上课记录ID:", cl_id_list)
                # ret = self.db.query(TablesInit.StudentRecords.qq_number).\
                #     filter(TablesInit.StudentRecords.class_record_id.in_(cl_id_list)).all()  # 返回的是元组对象
                # print("ret: ", ret)
                # # ret = self.db
                # qq_list = []
                # for qq in ret:
                #     qq_list.append(qq[0])
                # result = set(qq_list)
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
            elif type == 6:  # 根据学员name, 上课记录ID查询本次课的成绩排名
                rank = 0
                student_qq = self.db.query(TablesInit.Student.qq_number).filter_by(name=kwargs.get('st_name')).first()[0]
                # print("qq:", student_qq)
                result = self.db.query(TablesInit.StudentRecords).\
                    filter(TablesInit.StudentRecords.class_record_id == kwargs.get('cl_rc_id'),
                           TablesInit.StudentRecords.statue == 1).\
                    order_by(TablesInit.StudentRecords.score.desc()).all()  # 降序排列
                print("分数 | QQ号")
                for stu_rc in result:
                    print("%d    %s" % (stu_rc.score, stu_rc.qq_number))
                    if student_qq == stu_rc.qq_number:
                        rank = result.index(stu_rc) + 1
                result = rank
            return result
        except Exception as ex:
            print(ex)
            self.db.rollback()
            print("\033[33;1m操作异常\033[0m")

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
                class_list = []
                stu_info = self.db.query(TablesInit.Student).filter_by(name=kwargs.get('name')).all()
                for stu in stu_info:
                    for cls in stu.Class:
                        class_list.append(cls.name)
                result = class_list
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
            elif type == 7:
                # 学员上课记录表里找上课记录
                s_cls_rc = []
                m_cls_rc = []
                tc_id = self.db.query(TablesInit.Teacher.id).filter_by(name=kwargs.get('tc_name')).first()[0]  # 获取讲师ID
                result = self.db.query(TablesInit.StudentRecords.class_record_id).filter(
                    TablesInit.StudentRecords.qq_number == kwargs.get('qq')).all()
                # print(result)
                for cl_id in result:
                    s_cls_rc.append(cl_id[0])
                # 提交作业表里符合批改作业条件的上课记录ID
                name = self.db.query(TablesInit.Student.name).filter(TablesInit.Student.qq_number
                                                                     == kwargs.get('qq')).first()[0]
                # print(name)
                result = self.db.query(TablesInit.MissionRecords.class_record_id).filter(
                    TablesInit.MissionRecords.name == name,
                    TablesInit.MissionRecords.statue == 1).all()
                for cl_id in result:
                    m_cls_rc.append(cl_id[0])
                # print(s_cls_rc, m_cls_rc)
                # 根据两个记录的交集得出满足条件的上课记录
                result = self.db.query(TablesInit.ClassRecords).filter(TablesInit.ClassRecords.id.in_(
                    list(set(s_cls_rc).intersection(set(m_cls_rc)))),
                    TablesInit.ClassRecords.teacher_id == tc_id).all()
                # print(result)
            elif type == 8:
                # 根据学员的选择查找对应班级的上课记录
                class_rc_list = []
                m_cls_rc = []
                student_name = kwargs.get('st_name')
                class_name = kwargs.get('cl_name')
                # 获取该班级的所有上课记录ID
                class_info = self.db.query(TablesInit.Class).filter_by(name=class_name).all()
                for cl in class_info:
                    for class_rc_id in cl.ClassRecords:
                        class_rc_list.append(class_rc_id.id)
                # 获取学员QQ号
                student_qq = self.db.query(TablesInit.Student.qq_number).filter_by(name=student_name).first()[0]
                # 找到符合本学员查询成绩的上课记录
                result = self.db.query(TablesInit.StudentRecords.class_record_id).\
                    filter(TablesInit.StudentRecords.class_record_id.in_(class_rc_list),
                           TablesInit.StudentRecords.qq_number == student_qq,
                           TablesInit.StudentRecords.statue == 1).all()
                # print(result)
                for cl_id in result:
                    m_cls_rc.append(cl_id[0])
                result = self.db.query(TablesInit.ClassRecords).filter(TablesInit.ClassRecords.id.in_(m_cls_rc)).\
                    order_by(TablesInit.ClassRecords.course_id).all()  # 返回符合条件的上课记录
            elif type == 9:  # 根据上课记录ID查询分数
                # 获取学员QQ号
                student_qq = self.db.query(TablesInit.Student.qq_number).filter_by(name=kwargs.get('st_name')).first()[0]
                score = self.db.query(TablesInit.StudentRecords.score).\
                    filter_by(qq_number=student_qq, class_record_id=kwargs.get('cl_rc_id')).first()
                result = score[0]
            elif type == 10:  # 根据讲师姓名获取上课记录
                tc_id = self.db.query(TablesInit.Teacher.id).filter_by(name=kwargs.get('tc_name')).first()[0]  # 获取讲师ID
                result = self.db.query(TablesInit.ClassRecords).filter_by(teacher_id=tc_id).all()
            return result
        except Exception as ex:
            print(ex)
            self.db.rollback()
            print("\033[33;1m操作异常\033[0m")

    def modify(self, type, **kwargs):
        if type == 0:  # 修改上课记录
            pass
        elif type == 1:  # 修改学员成绩
            result = self.db.query(TablesInit.StudentRecords).filter_by(qq_number=kwargs.get('qq'),
                                                                        class_record_id=kwargs.get('cl_id')).first()
            result.statue = 1
            result.score = kwargs.get('score')
        try:
            self.db.commit()
            return 1
        except Exception as ex:
            print(ex)
            self.db.rollback()
            print("\033[33;1m操作异常\033[0m")
