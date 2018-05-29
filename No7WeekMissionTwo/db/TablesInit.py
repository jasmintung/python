# -*-coding:utf-8-*-
# author: zhangtong
# email: puzexiong@163.com
# instruction: 用sqlalchemy建表每个表必须有主键,规定!
import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from bin import database_config

print("初始化数据库")
print(database_config.USER_NAME)
print(database_config.PASSWORD)
# engine = create_engine("mysql+pymysql://root:sql2296990@localhost/world", encoding='utf-8', echo=True)
engine = create_engine("mysql+pymysql://%s:%s@localhost:%d/%s?charset=utf8" % (database_config.USER_NAME,
                                                                               database_config.PASSWORD,
                                                                               database_config.PORT,
                                                                               database_config.DATABASE_NAME
                                                                               ), encoding='utf-8', echo=True)

Base = declarative_base()  # 生成orm基类

# 讲师表


class Teacher(Base):
    __tablename__ = 'teacher'
    id = Column(Integer, unique=True, primary_key=True)
    name = Column(String(32))
    password = Column(String(32))

# 班级表


class Class(Base):
    __tablename__ = 'class'
    id = Column(Integer, unique=True, primary_key=True)
    name = Column(String(64))
    teacher_id = Column(Integer, ForeignKey('teacher.id'))
    qq_number = Column(String(16))

# 学员表


class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, unique=True, primary_key=True)
    name = Column(String(32))
    password = Column(String(64))
    qq_number = Column(String(16))

# 上课记录表


class ClassRecords(Base):
    __tablename__ = 'class_records'
    id = Column(Integer, unique=True, primary_key=True)  # 第几节课
    teacher_id = Column(Integer, ForeignKey('teacher.id'))  # 讲师
    class_id = Column(Integer, ForeignKey('class.id'))  # 哪个班级
    course_time = Column(String(64))  # 上课起止时间

# 学员上课记录表


class StudentRecords(Base):
    __tablename__ = 'student_records'
    id = Column(Integer, primary_key=True)
    statue = Column(Boolean)  # 0: 未完成 1: 完成
    score = Column(Integer)  # 作业得分
    class_record_id = Column(Integer, ForeignKey('class_records.id'))


# 学员作业提交表


class MissionRecords(Base):
    __tablename__ = 'mission_records'
    id = Column(Integer, primary_key=True)
    statue = Column(Boolean)  # 是否提交作业0:未提交, 1:提交
    class_record_id = Column(Integer, ForeignKey('class_records.id'))

Base.metadata.create_all(engine)  # 创建表结构
Session_class = sessionmaker(bind=engine)  # 创建与数据库的会话
Session = Session_class()  # 生成session实例
print(Session)


def getSQLDBHandler():
    return Session