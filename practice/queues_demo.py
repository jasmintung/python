# 队列
from multiprocessing import Process, Queue


def f(q):
    # 子进程写数据
    q.put([42, None, 'Hello'])

if __name__ == "__main__":
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    print(q.get()) # 父进程获取到子进程的数据
    p.join()
