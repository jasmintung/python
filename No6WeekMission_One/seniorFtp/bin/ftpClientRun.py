import os
import sys

proj_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(proj_dir)


from core import client_entry

if __name__ == '__main__':
    client_entry.main()
