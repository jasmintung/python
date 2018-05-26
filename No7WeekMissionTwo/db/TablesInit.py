import sqlalchemy
from sqlalchemy import Table, Column, MetaData, Integer, String, ForeignKey, create_engine
from bin import database_config

create_engine = create_engine("mysql+pymysql://%s:%s@localhost:%s/%scharset='utf-8'" % (database_config.USER_NAME,
                                                                                        database_config.PASSWORD,
                                                                                        database_config.PORT,
                                                                                        database_config.DATABASE_NAME
                                                                                        ), encoding='utf-8', echo=True)


# 获取元数据
metaData = MetaData()

users = Table('user', metaData,
             Column('id', Integer, primary_key=True),
             Column('name', String(20)),
             Column('fullname', String(40)),
             )
address = Table('address', metaData,
                Column('id', Integer, primary_key=True),
                Column('user_id', None, ForeignKey('user.id')),
                Column('email', String(60), nullable=False)
                )