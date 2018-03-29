#!usr/bin/env python
# -*- coding:utf-8 -*-
# auther:Tony Cheung
# 描述：window 环境下测试通过.
import os
import sys

proj_env = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(proj_env)

from core import FtpClient

if __name__ == '__main__':
    FtpClient.main()
