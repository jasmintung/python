import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE = {'dir': "%s/db/accounts/" % BASE_DIR}
SERVER_CONFIG = {"host": "127.0.0.1", "port": 9986}
LOCAL_DOWNLOAD_DRI = {"download_file_save_base_path": "C:\\Users\Public"}  # 客户端下载文件存放在本地的根路径
