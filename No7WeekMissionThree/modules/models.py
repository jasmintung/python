# -*- coding:utf-8 -*-
__author__ = 'zhangtong'

from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import ChoiceType,PasswordType

Base = declarative_base()  # 生成一个ORM 基类
# BindHost VS Group
BindHost2Group = Table('bindhost_2_group', Base.metadata,
                       Column('bindhost_id', ForeignKey('bind_host.id'), primary_key=True),
                       Column('group_id', ForeignKey('group.id'), primary_key=True))

# BindHost VS UserProfile
BindHost2UserProfile = Table('bindhost_2_userprofile', Base.metadata,
                             Column('bindhost_id', ForeignKey('bind_host.id'), primary_key=True),
                             Column('userprofile_id', ForeignKey('user_profile.id'), primary_key=True))

# Group VS UserProfile
Group2UserProfile = Table('bindhost_2_userprofile', Base.metadata,
                          Column('userprofile_id', ForeignKey('user_profile.id'), primary_key=True),
                          Column('group_id', ForeignKey('group.id'), primary_key=True))


class UserProfile(Base):
    """用户表"""
    __tablename__ = 'user_profile'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), unique=True, nullable=False)  # 用户名
    password = Column(String(128), unique=True, nullable=False)  # 密码
    Groups = relationship('Group', secondary=Group2UserProfile)
    bind_hosts = relationship('BindHost', secondary=BindHost2UserProfile)

    def __repr__(self):
        return "<UserProfile(id='%s', username='%s')>" % (self.id, self.username)


class RemoteUser(Base):
    """远程用户表"""
    __tablename__ = 'remote_user'
    AuthTypes = [('ssh-passwd', 'SSH/Password'),
                 ('ssh-key', 'SSH/KEY')]
    id = Column(Integer, primary_key=True)
    auth_type = Column(ChoiceType(AuthTypes))  # 鉴权方式
    username = Column(String(64), nullable=False)  # 用户名
    password = Column(String(255))  # 密码

    __table_args__ = (UniqueConstraint('auth_type', 'username', 'password', name='_user_passwd_uc_'),)  # 三个属性必须同时唯一

    def __repr__(self):
        return "<RemoteUser(id='%s', auth_type='%s', user='%s')>" % (self.id, self.username, self.password)


class Host(Base):
    """主机表"""
    __tablename__ = 'host'
    id = Column(Integer, primary_key=True)
    hostname = Column(String(64), unique=True, nullable=False)  # host 名称
    ip_addr = Column(String(128), unique=True, nullable=False)  # 主机IP地址
    port = Column(Integer, default=22)  # 端口号, 默认是22

    def __repr__(self):
        return "<Host(id='%s', hostname='%s')>" % (self.id, self.hostname)


class Group(Base):
    """组表"""
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)  # 组名
    bind_host = relationship("BindHost", secondary=BindHost2Group)
    user_profiles = relationship("UserProfile", secondary=Group2UserProfile)

    def __repr__(self):
        return "<Group(id='%s', name='%s')>" % (self.id, self.name)


class BindHost(Base):
    """绑定表"""
    __tablename__ = 'bind_host'
    id = Column(Integer, primary_key=True)
    host_id = Column(Integer, ForeignKey('host.id'))  # 外键关联主机ID
    remote_user_id = Column(Integer, ForeignKey('remote_user.id'))  # 外键关联远程用户ID

    host = relationship("bind_host")
    remoteuser = relationship("RemoteUser")
    groups = relationship("Group", secondary=BindHost2Group, back_populates='bind_hosts')
    __table_args__ = (UniqueConstraint('host_id', 'remote_user_id', name='_bindhost_and_user_uc'))  # 属性同时唯一

    def __repr__(self):
        return "<BindHost(id='%s', name='%s', user='%s')>" % (self.id, self.host_id, self.remote_user_id)


class AuditLog(Base):
    """操作记录表"""
    __tablename__ = 'audit_log'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_profile.id'))
    bind_host_id = Column(Integer, ForeignKey('bind_host.id'))
    user_profile = relationship("UserProfile")
    bind_host = relationship("BindHost")