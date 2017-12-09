class RoleBase(object):

    def __init__(self, user_name, password, authority_level):  # Constructor of the class
        self.user_name = user_name  # 登陆用户名
        self.password = password  # 登陆密码
        self.authority_level = authority_level  # 角色权限等级
        self.down_upload_level = 0  # 下载上传等级
        self.current_view_dst = ""  # 当前停留在的绝对目录路径
        self.current_view_file = ""  # 当前要操作的文件

    def get_user_name(self):
        """
        获得当前登陆的用户名
        :return:
        """
        return self.user_name

    def get_password(self):
        """
        获得当前登陆的密码
        :return:
        """
        return self.password

    def set_authority_level(self, level):
        """
        设置当前登陆用户的访问等级
        :param level: 1: Real, 2: Guest, 9: Admin
        :return:
        """
        self.authority_level = level

    def get_authority_level(self):
        """
        返回当前登陆用户的访问等级
        :return:
        """
        return self.authority_level

    def set_down_upload_level(self, level):
        """
        设置当前登陆用户的下载上传等级
        :param level: 0: 都不支持, 1: down, 2: upload, 3: Both 1 and 2
        :return:
        """
        self.down_upload_level = level

    def get_down_upload_level(self):
        """
        返回当前登陆用户的下载上传等级
        :return:
        """
        return self.down_upload_level

