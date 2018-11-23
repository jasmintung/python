"""
Coroutine closing demonstration::

# BEGIN DEMO_CORO_EXC_1
    >>> exc_coro = demo_exc_handling()
    >>> next(exc_coro)
    -> coroutine started
    >>> exc_coro.send(11)
    -> coroutine received: 11
    >>> exc_coro.send(22)
    -> coroutine received: 22
    >>> exc_coro.close()
    >>> from inspect import getgeneratorstate
    >>> getgeneratorstate(exc_coro)
    'GEN_CLOSED'

# END DEMO_CORO_EXC_1

Coroutine handling exception::

# BEGIN DEMO_CORO_EXC_2
    >>> exc_coro = demo_exc_handling()
    >>> next(exc_coro)
    -> coroutine started
    >>> exc_coro.send(11)
    -> coroutine received: 11
    >>> exc_coro.throw(DemoException)
    *** DemoException handled. Continuing...
    >>> getgeneratorstate(exc_coro)
    'GEN_SUSPENDED'

# END DEMO_CORO_EXC_2

Coroutine not handling exception::

# BEGIN DEMO_CORO_EXC_3
    >>> exc_coro = demo_exc_handling()
    >>> next(exc_coro)
    -> coroutine started
    >>> exc_coro.send(11)
    -> coroutine received: 11
    >>> exc_coro.throw(ZeroDivisionError)
    Traceback (most recent call last):
      ...
    ZeroDivisionError
    >>> getgeneratorstate(exc_coro)
    'GEN_CLOSED'

# END DEMO_CORO_EXC_3
"""

# BEGIN EX_CORO_EXC


class DemoException(Exception):
    """An exception type for the demonstration."""


def demo_exc_handling():
    print('-> coroutine started')
    try:  # 使用try/finally块在协程终止时执行操作
        while True:
            try:
                x = yield
            except DemoException:  # <1>
                print('*** DemoException handled. Continuing...')
            else:  # <2>
                print('-> coroutine received: {!r}'.format(x))
        raise RuntimeError('This line should never run.')  # <3>
    finally:
        print('->coroutine ending')
# END EX_CORO_EXC


exc_coro = demo_exc_handling()
print("------")
next(exc_coro)
print("++++++")
print(exc_coro.send(11))
print(exc_coro.send(22))
exc_coro.close()
from inspect import getgeneratorstate
print(getgeneratorstate(exc_coro))
# ------
# -> coroutine started
# ++++++
# -> coroutine received: 11
# None
# -> coroutine received: 22
# None
# GEN_CLOSED

print("*"*15)

exc_coro1 = demo_exc_handling()
next(exc_coro1)
print(exc_coro1.send(11))
print(exc_coro1.throw(DemoException))
print(getgeneratorstate(exc_coro1))
# -> coroutine started
# -> coroutine received: 11
# None
# *** DemoException handled. Continuing...
# None
# GEN_SUSPENDED


# 如果传入协程的异常没有处理,协程会停止，即状态变成'GEN_CLOSED'


print("*"*15)

exc_coro2 = demo_exc_handling()
next(exc_coro2)
print(exc_coro2.send(11))
print(exc_coro2.throw(ZeroDivisionError))
print(getgeneratorstate(exc_coro2))
# Traceback (most recent call last):
# ....
# GEN_CLOSED
# ZeroDivisionError
