#!/usr/bin/env python3

# spinner_asyncio.py

# credits: Example by Luciano Ramalho inspired by
# Michele Simionato's multiprocessing example in the python-list:
# https://mail.python.org/pipermail/python-list/2009-February/538048.html

# BEGIN SPINNER_ASYNCIO
# 要求：1、必须使用yield from。2、asyncio的协程要由调用方驱动，并由调用方通过yield from调用，或把协程传给asyncio包
# 中的某个函数，从而驱动协程。3、@asyncio.coroutine装饰器必须要用
import asyncio
import itertools
import sys


@asyncio.coroutine  # <1>
def spin(msg):  # <2>
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        try:
            yield from asyncio.sleep(.1)  # <3>替代time.sleep()，这样的休眠不会阻塞时间循环
        except asyncio.CancelledError:  # <4>
            break
    write(' ' * len(status) + '\x08' * len(status))


@asyncio.coroutine
def slow_function():  # <5>
    # pretend waiting a long time for I/O模拟I/O操作
    yield from asyncio.sleep(3)  # <6>把控制权交给主循环，休眠结束后恢复这个协程。
    return 42


@asyncio.coroutine
def supervisor():  # <7>
    spinner = asyncio.async(spin('thinking!'))  # <8>排定spin协程运行时间
    print('spinner object:', spinner)  # <9>
    result = yield from slow_function()  # <10>驱动slow_function()。结束后，获取返回值，事件循环继续运行.
    spinner.cancel()  # <11>在协程当前暂停的yield出抛出asyncio.CancelledError异常。协程可捕获这个异常，也可延迟取消
    return result


def main():
    loop = asyncio.get_event_loop()  # <12>获取事件循环的引用
    result = loop.run_until_complete(supervisor())  # <13>驱动supervisor协程,让它运行完毕
    loop.close()
    print('Answer:', result)


if __name__ == '__main__':
    main()
# END SPINNER_ASYNCIO
