# -*-coding:utf-8-*-
__author__ = 'zhangtong'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from conf import settings

engine = create_engine(settings.DB_CONN)
SessionCls = sessionmaker(bind=engine)
session = SessionCls()
