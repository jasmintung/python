from core import RoleBase


class Admin(RoleBase):
    """管理员类"""
    def __init__(self, login_id, password):
        super(Admin, self).__init__(login_id, password)

    def create_role(self):
        """创建用户"""
        pass

    def allocate_disk_space(self):
        """分配磁盘配额"""
        pass
