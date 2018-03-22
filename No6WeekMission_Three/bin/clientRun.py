import os
import sys

proj_env = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(proj_env)

from core import FtpClient

if __name__ == '__main__':
    FtpClient.main()
