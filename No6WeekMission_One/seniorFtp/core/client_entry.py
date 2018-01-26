from core import FtpClient
from core import User


def main():
    print("******登陆FTP服务器******")
    host = input("请输入IP: ")
    port = int(input("请输入端口: "))
    instance_client = FtpClient.FtpClient(host, port)
    instance_client.client_init()
    instance_client.request()

    instance_role = User.User()
    instance_role.auth()