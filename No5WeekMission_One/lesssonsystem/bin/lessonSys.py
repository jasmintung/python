import os
import sys
# 配置系统环境变量
proj_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(proj_dir)
# 程序入口
from core import main

if __name__ == '__main__':
    main.run()
