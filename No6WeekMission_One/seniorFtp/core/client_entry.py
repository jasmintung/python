import threading
from core import FtpClient
from core import User
from core import RoleBase
protocol = {"account": "", "password": "", "cmd": "", "data": ""}


# def new_thread(choice, conn, role):
#     """创建线程"""
#     ready_get_server = True
#     tup_params = ()
#     if choice == '2':
#         local_save_path = role.download_file_request(conn)  # 下载文件流程
#         if not local_save_path:
#             ready_get_server = False
#         else:
#             tup_params = (local_save_path, )
#     elif choice == '3':
#         path, size = role.upload_file_request(conn)  # 上传文件流程
#         if not path:
#             ready_get_server = False
#         else:
#             tup_params = (path, size, )
#
#     elif choice == '4':
#         role.download_multi_files(conn)  # 多文件下载流程
#     elif choice == '5':
#         role.upload_multi_files(conn)  # 多文件上传流程
#     elif choice == '6':
#         role.resume_tasks(conn)  # 断电续传流程
#     else:
#         print("选择错误!")
#         ready_get_server = False
#     if ready_get_server:
#         role.deal_server_response_datas(conn, tup_params)


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
            user_pwd = input("输入密码")
            client = FtpClient.FtpClient(host, port)
            client.new_socket()
            instance_role = User.User(client, user_id, user_pwd)
            instance_role.request_auth('user')
            instance_role.deal_server_response_datas(client, None)
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
                    4. 多文件下载
                    5. 多文件上传
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
                        elif func_choice == '4':
                            instance_role.download_multi_files()  # 多文件下载流程
                        elif func_choice == '5':
                            instance_role.upload_multi_files()  # 多文件上传流程
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
