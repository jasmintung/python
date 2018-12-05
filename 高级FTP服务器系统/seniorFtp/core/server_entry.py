from core import FtpServer
from conf import settings


def main():
    print("init server")
    instance_server = FtpServer.FtpServer(settings.source_dist.get("server_ip"),
                                          settings.source_dist.get("server_port"))
    instance_server.server_init()

