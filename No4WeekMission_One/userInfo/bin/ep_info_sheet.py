import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(base_dir)
sys.path.append(base_dir)  # 把自定义环境动态加载到python环境里面

from core import main

if __name__ == '__main__':
    main.run()