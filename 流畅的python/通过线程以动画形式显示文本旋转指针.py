#!/usr/bin/env python3

# spinner_thread.py

# credits: Adapted from Michele Simionato's
# multiprocessing example in the python-list:
# https://mail.python.org/pipermail/python-list/2009-February/538048.html

# BEGIN SPINNER_THREAD
import threading
import itertools
import time
import sys


def spin(msg, done):  # <2>在单独的线程中运行
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):  # <3>itertools.cycle函数会从指定的序列中反复不断生成元素
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))  # <4>使用退格符(\x08)把光标移回来
        if done.wait(.1):  # <5>
            break
    write(' ' * len(status) + '\x08' * len(status))  # <6>


def slow_function():  # <7>
    # pretend waiting a long time for I/O
    time.sleep(3)  # <8>
    return 42


def supervisor():  # <9>
    done = threading.Event()
    spinner = threading.Thread(target=spin,  # 创建从属线程
                               args=('thinking!', done))
    print('spinner object:', spinner)  # <10>
    spinner.start()  # <11>  # 启动从属线程
    result = slow_function()  # <12>  # 阻塞主线程。同时从属线程开始工作
    done.set()  # <13>
    spinner.join()  # <14>  # 等待从属线程结束
    return result


def main():
    result = supervisor()  # <15>
    print('Answer:', result)


if __name__ == '__main__':
    main()
# END SPINNER_THREAD
