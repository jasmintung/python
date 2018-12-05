# -*- coding:utf-8 -*-
from django.db import models

# Create your models here.
from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()  # 生成一个ORM基类


class StaffInfo(Base):
    """员工信息表"""
    __tablename__ = 'staff_info'  # 这个名字是在数据库中的表名
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)  # 姓名
    id_number = Column(String(32), nullable=False)  # 身份证号
    origin = Column(String(16), nullable=False)  # 籍贯
    age = Column(Integer, nullable=False)  # 年龄
    sex = Column(String(8), nullable=False)  # 性别
    position = Column(String(32), nullable=False)  # 职位
    address = Column(String(128))  # 住址
    phone = Column(String(32))  # 电话

    def __repr__(self):
        return "<StaffInfo(id='%s', name='%s')>" % (self.id, self.name)


class UserInfo(Base):
    """用户表"""
    __tablename__ = 'user_info'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), unique=True, nullable=False)  # 用户名
    password = Column(String(64), nullable=False)  # 密码

    def __repr__(self):
        return "<UserInfo(id='%s', name='%s')>" % (self.id, self.username)


engine = create_engine("mysql+pymysql://root:sql2296990@localhost:3306/staffmanagedb?charset=utf8", encoding='utf-8')
SessionCls = sessionmaker(bind=engine)
session = SessionCls()
Base.metadata.create_all(engine)  # 创建表
