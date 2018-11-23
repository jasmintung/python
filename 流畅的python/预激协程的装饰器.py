from functools import wraps


def coroutine(func):
    """装饰器：向前执行到第一个yield表达式,预激;func"""
    def primer(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen
    return primer


@coroutine
def average():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield average  # 这里的average作为返回值(产出值)返回给客户端
        total += term
        count += 1
        average = total/count


coro_avg = average()
from inspect import getgeneratorstate
print(getgeneratorstate(coro_avg))
print(coro_avg.send(10))  # 10.0
print(coro_avg.send(30))  # 20.0
print(coro_avg.send(5))  # 30.0
