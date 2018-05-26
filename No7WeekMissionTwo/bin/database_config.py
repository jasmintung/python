import os, sys

BASE_PROJ_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PROJ_DIR)

USER_NAME = "root"  # 数据库连接用户名
PASSWORD = "sql2296990"  # 数据库连接密码
PORT = 3306
DATABASE_NAME = "StudentManagement"
