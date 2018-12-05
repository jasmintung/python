# Manager是一种较为高级的多进程通信方式，它能支持Python支持的的任何数据结构。
# 它的原理是：先启动一个ManagerServer进程，这个进程是阻塞的，它监听一个socket，然后其他进程（ManagerClient）通过socket来连接到ManagerServer，实现通信
# Python实现多进程间通信的方式有很多种，例如队列，管道等。
# 但是这些方式只适用于多个进程都是源于同一个父进程的情况
# 如果多个进程不是源于同一个父进程，只能用共享内存，信号量等方式，但是这些方式对于复杂的数据结构，例如Queue，dict，list等，使用起来比较麻烦，不够灵活
# Python通过Manager方式实现多个无关联进程共享数据
from multiprocessing import Process, Manager
import os


def f(d, l):
    print(l)
    d[os.getpid()] = os.getpid()
    d['2'] = 2
    d[0.25] = None
    l.append(l)
    # print(l)


if __name__ == "__main__":
    with Manager() as manager:
        d = manager.dict()

        l = manager.list(range(5))
        p_list = []
        for i in range(10):
            # print(l)
            p = Process(target=f, args=(d, l))
            p.start()
            p_list.append(p)
        for res in p_list:
            res.join()

        # print(d)
        print(l)
