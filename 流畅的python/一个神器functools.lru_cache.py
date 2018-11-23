# 生成第n个斐波拉契数,使用递归
# 正常写法:
from clockdeco import clock


@clock
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-2) + fibonacci(n-1)


# 优化后:
import functools


@functools.lru_cache()
@clock
def fibonacci_2(n):
    if n < 2:
        return n
    return fibonacci_2(n-2) + fibonacci_2(n-1)


if __name__ == '__main__':
    print(fibonacci(30))
    print(fibonacci_2(30))
