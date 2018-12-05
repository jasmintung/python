import os
import sys

PROJ_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJ_DIR)

from core import ServerEntry

if __name__ == '__main__':
    ServerEntry.main()
