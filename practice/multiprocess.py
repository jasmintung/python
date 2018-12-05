from multiprocessing import Process
import time
import os


def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())
    print("\n\n")


def f(name):
    time.sleep(2)
    print('hello', name)

if __name__ == "__main__":
    p = Process(target=info, args=('zhangtong', ))
    p.start()
    p.join()
