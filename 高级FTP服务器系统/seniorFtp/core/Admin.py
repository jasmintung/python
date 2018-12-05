from core import RoleBase


class Admin(RoleBase):
    """管理员类"""
    def __init__(self, conn):
        super(Admin, self).__init__(conn)
        self.conn = conn

    def create_role(self):
        """创建用户"""
        pass

    def allocate_disk_space(self):
        """分配磁盘配额"""
        pass

