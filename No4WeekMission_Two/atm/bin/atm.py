# __author__:"zhangtong"
import os
import sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)  # 将路径加入到python环境变量里面
print(base_dir)

from core import main

if __name__ == '__main__':
    main.run()
