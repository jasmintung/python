from core import RoleBase


class User(RoleBase):
    """普通用户类"""
    def __init__(self, login_id, password):
        super(User, self).__init__(login_id, password)
        self.upload_files_list = {}
        self.download_files_list = {}

    def view_files(self):
        """访问目录及文件"""
        pass

    def upload_file(self):
        """单任务上传"""
        pass

    def upload_multi_files(self):
        """多任务上传"""
        pass

    def download_file(self):
        """单任务下载"""
        pass

    def download_multi_files(self):
        """多任务下载"""
        pass

    def resume_tasks(self):
        """断点续传"""
        pass
