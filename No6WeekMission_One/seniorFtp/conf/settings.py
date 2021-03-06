import os
import re

server_ip = "127.0.0.1"
port = 9986
PROJ_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SYS_BASE_DISK_DIR = ""  # Linux中程序所在系统的根目录,windows中程序所在系统的盘符的根目录
if os.name == "nt":  # windows
    SYS_BASE_DISK_DIR = re.match(r"\D:\\", PROJ_BASE_DIR).group()
elif os.name == "posix":  # Linux
    SYS_BASE_DISK_DIR = re.match(r"\D:/", PROJ_BASE_DIR).group()
DOWNLOAD_RC_FILE_NAME = "dwnrc.txt"
UPLOAD_RC_FILE_NAME = "uprc.txt"

source_dist = {"account_path": "%s" % PROJ_BASE_DIR + os.sep + "db" + os.sep + "accounts",
               "download_record_dir": "%s" % PROJ_BASE_DIR + os.sep + "db" + os.sep + "download_record",
               "upload_record_dir": "%s" % PROJ_BASE_DIR + os.sep + "db" + os.sep + "upload_record",
               "server_ip": server_ip,
               "server_port": port,
               "base_disk_path": SYS_BASE_DISK_DIR,
               "proj_base_path": PROJ_BASE_DIR}
size_control = {"leveA": 1024, "leveB": 2048, "leveC": 4096, "leveD": 5120, "leveE": 10*1204, "leveF": 20*1024}
