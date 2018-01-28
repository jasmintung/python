from core import FtpClient
from core import User
from core import Admin

def main():
    print("******登陆FTP服务器******")
    host = input("请输入IP: ")
    port = int(input("请输入端口: "))
    instance_client = FtpClient.FtpClient(host, port)
    instance_client.client_init()

    instance_role = None
    login_notice = """
    请选择您的登录角色:
    1、普通用户登录
    0、管理员登录
    """
    print(login_notice)
    choice = input(">>").strip()
    if choice == '1':
        instance_role = User.User()
        instance_role.request_auth('user')
    elif choice == '0':
        instance_role = Admin.Admin()
        instance_role.request_auth('admin')
    while True:
        if not instance_client.get_response():
            continue

