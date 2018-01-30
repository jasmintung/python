import threading
from core import FtpClient
from core import User
from core import Admin
from core import common_func
protocol = {"account": "", "password": "", "cmd": "", "data": ""}


def new_socket(host, port):
    """创建一个socket"""
    instance_client = FtpClient.FtpClient(host, port)
    instance_client.client_init()
    return instance_client.conn

def new_thread(choice, conn, instance_role):
    """创建线程"""
    ready_get_server = True
    if choice == '2':
        instance_role.download_file(conn)
    elif choice == '3':
        ready_get_server = instance_role.upload_file_request(conn)
    elif choice == '4':
        instance_role.download_multi_files(conn)
    elif choice == '5':
        instance_role.upload_multi_files(conn)
    elif choice == '6':
        instance_role.resume_tasks(conn)
    else:
        print("选择错误!")
    if ready_get_server:
        instance_role.deal_server_response_datas()
def main():
    print("******登陆FTP服务器******")
    host = input("请输入IP: ")
    port = int(input("请输入端口: "))

    while True:
        instance_role = None
        login_notice = """
        请选择您的登录角色:
        1、登录
        8、退出
        """
        print(login_notice)
        choice = input(">>").strip()
        if choice == '1':
            sk = new_socket(host, port)
            instance_role = User.User()
            instance_role.request_auth('user', sk)
            if instance_role.deal_server_response_datas(sk) == 1:
                instance_role.login_statue = 1
        elif choice == '8':
            exit()

        while True:
            if instance_role.login_statue == 1:
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
                if func_notice == '1' or func_notice == '8':
                    if func_notice == '1':
                        instance_role.view_files_request()
                    if func_notice == '8':
                        exit()
                else:
                    t = threading.Thread(target=new_thread, args=(int(func_choice), new_socket(), instance_role))
                    t.start()


