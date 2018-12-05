import threading
import sys, signal
import os
from core import FtpClient
from core import User
from core import RoleBase

protocol = {"account": "", "password": "", "cmd": "", "data": ""}
sys.setrecursionlimit(1000000)  # 设置递归深度


def shutdown_task(signum, frame):
    print("taks shutdown!")

print(threading.current_thread().getName())
print(os.getpid())
print(os.getppid())

def create_signal():
    """pycharm下不适用"""
    try:
        signal.signal(signal.SIGINT, shutdown_task)
        signal.signal(signal.SIGTERM, shutdown_task)
        while True:
            pass
    except Exception as exc:
        print(exc)


def main():
    print("******登陆FTP服务器******")
    host = input("请输入IP: ")
    port = int(input("请输入端口: "))

    while True:
        login_notice = """
        请选择:
        1、登陆
        8、退出
        """
        print(login_notice)
        choice = input(">>").strip()
        if choice == '1':
            user_id = input("输入用户名:")
            user_pwd = input("输入密码:")
            # user_id = "jack"
            # user_pwd = "123456"
            # host = "127.0.0.1"
            # port = 9986
            client = FtpClient.FtpClient(host, port)
            rs = client.new_socket()
            if not rs:
                print("\033[34;1m链接服务器异常\033[0m")
                break
            instance_role = User.User(client, user_id, user_pwd)
            instance_role.request_auth('user')
            instance_role.deal_server_response_datas(client, None)
            # s = threading.Thread(target=create_signal) # 用于ctrl+C退出程序使用
            # s.start()
            while True:
                if RoleBase.RoleBase.is_login:
                    instance_role.show_cur_files()
                    # 登陆成功后依次打印出home路径,及home路径下的子目录、文件夹、文件的名字
                    # print(instance_role.get_cur_view_path())
                    # print(" ".join(instance_role.get_dir_files().split(",")))
                    func_notice = """
                    请根据 编号(1~5)选择功能操作:
                    1. 访问其它目录
                    2. 下载文件
                    3. 上传文件
                    8. 退出
                    """
                    print(func_notice)
                    func_choice = input(">>").strip()
                    if func_choice == '1' or func_choice == '8':
                        if func_choice == '1':
                            print("访问其它目录")
                            instance_role.view_files_request()
                            instance_role.deal_server_response_datas(client, None)
                        if func_choice == '8':
                            print("退出程序")
                            exit()
                    else:
                        if func_choice == '2':
                            instance_role.download_file_request()  # 下载文件流程
                        elif func_choice == '3':
                            instance_role.upload_file_request()  # 上传文件流程
                        # elif func_choice == '4':
                        #     instance_role.download_multi_files()  # 多文件下载流程
                        # elif func_choice == '5':
                        #     instance_role.upload_multi_files()  # 多文件上传流程
                        else:
                            print("选择错误")
                        # t = threading.Thread(target=new_thread,
                        #                      args=(func_choice, new_socket(host, port), instance_role,))
                        # t.start()
                else:
                    break
        elif choice == '8':
            exit()
        else:
            print("选择不正确!")
