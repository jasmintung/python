import threading
from core import FtpClient
from core import User
from core import Admin
from core import common_func
protocol = {"account": "", "password": "", "cmd": "", "data": ""}


def main():
    print("******登陆FTP服务器******")
    host = input("请输入IP: ")
    port = int(input("请输入端口: "))
    instance_client = FtpClient.FtpClient(host, port)
    instance_client.client_init()
    while True:
        instance_role = None
        login_notice = """
        请选择您的登录角色:
        1、普通用户登录
        0、管理员登录
        8、退出
        """
        print(login_notice)
        choice = input(">>").strip()
        if choice == '1':
            instance_role = User.User(instance_client)
            instance_role.request_auth('user')
        elif choice == '0':
            instance_role = Admin.Admin(instance_client)
            instance_role.request_auth('admin')
        elif choice == '8':
            exit()
        if instance_role.get_login_statue():
            while True:
                if choice == '1':
                    # 登陆成功后依次打印出home路径,及home路径下的子目录、文件夹、文件的名字
                    print(instance_role.get_default_home_path())
                    print(" ".join(instance_role.get_dir_files().split(",")))
                    ready_get_datas = True
                    func_notice = """
                    请根据 编号(1~5)选择功能操作:
                    1. 访问其它目录
                    2. 下载文件
                    3. 上传文件
                    4. 多文件下载
                    5. 多文件上传
                    6. 续传文件
                    8. 退出
                    """
                    print(func_notice)
                    func_choice = input(">>").strip()
                    if func_notice == '1':
                        instance_role.view_files_request()
                    elif func_notice == '2':
                        instance_role.download_file()
                    elif func_notice == '3':
                        ready_get_datas = instance_role.upload_file_request()
                    elif func_notice == '4':
                        instance_role.download_multi_files()
                    elif func_notice == '5':
                        instance_role.upload_multi_files()
                    elif func_notice == '6':
                        instance_role.resume_tasks()
                    elif func_notice == '8':
                        exit()
                    else:
                        print("选择错误!")
                    if ready_get_datas is False:
                        continue
                elif choice == '0':
                    func_notice = """
                        请根据 编号(1~2)选择功能操作:
                        1、创建用户
                        2、分配磁盘空间
                        8、退出
                        """
                    print(func_notice)
                    func_choice = input(">>").strip()
                    if func_notice == '1':
                        instance_role.create_role()
                    elif func_notice == '2':
                        instance_role.allocate_disk_space()
                    elif func_notice == '8':
                        exit()
                    else:
                        print("选择错误!")
                recv_datas = eval(str(instance_client.get_response().decode()))
                instance_role.process_server_response(recv_datas)
