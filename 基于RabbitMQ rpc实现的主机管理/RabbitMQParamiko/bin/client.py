import os
import sys

PROJ_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJ_DIR)  # 将项目路径加入到环境变量

from core import ClientEntry

if __name__ == '__main__':
    ClientEntry.main()
