# mysql中属性的长度需要制定,SQLite and PostgreSQL不需要指定
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, select
from sqlalchemy.sql import and_, or_, not_

print(sqlalchemy.__version__)

# 连接数据库,这个时候的返回还没有真的去连接数据库
engine = create_engine("mysql+pymysql://root:sql2296990@localhost:3306/ztbd?charset=utf-8", encoding='utf-8', echo=True)
# 获取元数据
metadata = MetaData()
# 定义表
users = Table('user', metadata,
             Column('id', Integer, primary_key=True),
             Column('name', String(20)),
             Column('fullname', String(40)),
             )
address = Table('address', metadata,
                Column('id', Integer, primary_key=True),
                Column('user_id', None, ForeignKey('user.id')),
                Column('email', String(60), nullable=False)
                )
# 创建数据表,如果数据表存在,则忽视
metadata.create_all(engine)
# 对应的SQL语句
# CREATE TABLE users (
#     id INTEGER NOT NULL,
#     name VARCHAR,
#     fullname VARCHAR,
#     PRIMARY KEY (id)
# )
# ()
# COMMIT
# CREATE TABLE addresses (
#     id INTEGER NOT NULL,
#     user_id INTEGER,
#     email VARCHAR NOT NULL,
#     PRIMARY KEY (id),
#     FOREIGN KEY(user_id) REFERENCES users (id)
# )
# ()
# COMMIT
# 获取数据库连接
conn = engine.connect()
ins = users.insert()  # 使用查询
user_info = dict(name='jack', fullname='jack Jone')
r = conn.execute(ins, **user_info)  # 第一个是查询对象,第二个参数为一个插入数据字典,如果插入的是多个对象,就把对象字典放在列表里面
print(r)
ins = address.insert()
# 插入多条记录
r = conn.execute(ins, [{'user_id': 1, 'email': 'jack@yahoo.com'},
                   {'user_id': 1, 'email': 'jack@msn.com'},
                   {'user_id': 2, 'email': 'www@www.org'},
                   {'user_id': 2, 'email': 'wendy@aol.com'},
                   ])
print(r)
print(r.rowcount)  # 返回影响的行数
ins = users.insert().values(name='tom', fullname='tom Jim')
print(ins.compile())
# 通过编译方式来查看这些数据
print(ins.compile().params)
r = conn.execute(ins)
print(r.rowcount)
# 查询select
s = select([users])
result = conn.execute(s)
# 对应SQL语句
# SELECT users.id, users.name, users.fullname
# FROM users
# ()
for row in result:
    print(row)
# 输出如下: 元组
# (1, u'jack', u'Jack Jones')
# (2, u'wendy', u'Wendy Williams')
result = conn.execute(s)
row = result.fetchone()
print("name:", row['name'], "; fullname:", row['fullname'])
# 输出如下
# name: jack ; fullname: Jack Jones
row = result.fetchone()
print("name:", row[1], "; fullname:", row[2])
# 输出如下
# name: wendy ; fullname: Wendy Williams
for row in conn.execute(s):
    print("name:", row[users.c.name], "; fullname:", row[users.c.fullname])
# 输出如下
# name: jack ; fullname: Jack Jones
# name: wendy ; fullname: Wendy Williams
s = select([users, address]).where(users.c.id == address.c.user_id)
for row in conn.execute(s):
    print(row)
# 操作符
print(users.c.id == address.c.user_id)
# 输出结果:<sqlalchemy.sql.elements.BinaryExpression object at 0x...>
print(str(users.c.id == address.c.user_id))
# 输出结果:'users.id = addresses.user_id'

print(and_(
    users.c.name.like('j%'),
    users.c.id == address.c.user_id,
    or_(
        address.c.email == 'wendy@aol.com',
        address.c.email == 'jack@yahoo.com'
    ),
    not_(users.c.id > 5)
))
# users.name LIKE :name_1 AND users.id = addresses.user_id AND
# (addresses.email_address = :email_address_1
#    OR addresses.email_address = :email_address_2)
# AND users.id <= :id_1
print(
    users.c.name.like('j%') & (users.c.id == address.c.user_id) &
    (
        (address.c.email == 'wendy@aol.com') |
        (address.c.email == 'jack@yahoo.com')
    )
    & ~(users.c.id > 5)
)
# users.name LIKE :name_1 AND users.id = addresses.user_id AND
# (addresses.email_address = :email_address_1
#     OR addresses.email_address = :email_address_2)
# AND users.id <= :id_1
