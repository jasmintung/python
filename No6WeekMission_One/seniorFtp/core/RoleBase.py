from conf import settings
import os
protocol = {"account": "", "password": "", "cmd": "", "data": ""}


class RoleBase(object):
    """角色基类"""
    account_dir = settings.source_dist.get("account_path")
    account_id = ""  # 用户ID
    account_pwd = ""  # 用户密码
    home_dir = ""  # 默认用户home目录绝对路径
    is_login = False  # 登陆状态

    def __init__(self):
        self.is_login = False
        self.view_path = ""  # 当前用户访问的目录绝对路径,根据需求要求的权限设定: 一定是以home目录开始的字符串
        self.dir_files = ""  # 路径下的文件及文件夹及子目录名集合,通过','号隔开

    # @login('request')
    def request_auth(self, role_type, conn):
        protocol["account"] = RoleBase.account_id
        protocol["password"] = RoleBase.account_pwd
        protocol["cmd"] = "login"
        protocol["data"] = role_type
        self.request_server(protocol, conn)

    # @login('admin')
    def a_auth(self):
        admin_dir = ""
        admin_dir = RoleBase.account_dir + settings.source_dist.get("admin_pack_name")
        admin_path = ""
        admin_path = admin_dir + self.account_id
        return self.account_check(admin_path)

    # @login('user')
    def u_auth(self):
        user_dir = ""
        user_dir = RoleBase.account_dir + settings.source_dist.get("user_pack_name")
        user_path = ""
        user_path = user_dir + self.account_id
        return self.account_check(user_path)

    def account_check(self, path):
        if os.path.exists(path) is False:
            """账户不存在"""
            return 0
        else:
            if os.path.isfile(path):
                pass
            else:
                """账户异常"""
                return -1

    def analysis_protocol(self, args):
        recv_datas = b''
        if len(args) > 0:
            recv_datas = eval(str(args.decode()))
            return recv_datas.get("cmd"), recv_datas.get("data")

    def update_login_statue(self, args):
        """更新用户登陆状态"""
        RoleBase.is_login = args

    def set_default_home_path(self, args):
        """设置用户默认home路径"""
        RoleBase.home_dir = args

    def get_default_home_path(self):
        """获取用户默认home路径"""
        return RoleBase.home_dir

    def set_cur_view_path(self, args):
        """设置当前访问路径"""
        self.view_path = args

    def get_cur_view_path(self):
        """获取当前访问路径"""
        return self.view_path

    def set_dir_files(self, args):
        """保存当前路径下的所有子目录及文件名"""
        self.dir_files = args

    def get_dir_files(self):
        """获取当前路径下的所有子目录及文件名"""
        return self.dir_files

    def set_account(self, uid, password):
        RoleBase.account_id = uid
        RoleBase.account_pwd = password

    @staticmethod
    def request_server(args, conn):
        """告知服务器发送数据长度角色类发送接口"""
        conn.send_request_length(args)  # 先告诉将要发送数据的长度
        server_final_ack = conn.get_response()  # 等待响应
        print("server response:", server_final_ack.decode())
        conn.send_request(args)  # 发送数据
