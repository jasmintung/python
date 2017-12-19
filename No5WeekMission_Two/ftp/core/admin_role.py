from core import role
# FTP服务器管理员类


class Admin(role.RoleBase):

    def __init__(self, user_name, password):
        super(Admin, self).__init__(user_name, password, 9)

    def create_user(self):  # 创建普通用户
        pass
