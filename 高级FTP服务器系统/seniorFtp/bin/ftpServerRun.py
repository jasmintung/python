import sys
import os
proj_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(proj_dir)


from core import server_entry

if __name__ == '__main__':
    server_entry.main()
