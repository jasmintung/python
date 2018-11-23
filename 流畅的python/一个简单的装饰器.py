import time


def clock(func):
    def clocked(*args):
        t0 = time.perf_counter()
        result = func(*args)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result
    return clocked


@clock
def factorial(n):
    return 1 if n < 2 else n * factorial(n - 1)


if __name__ == '__main__':
    print("*" * 40, 'Calling factorial(6)')
    print('6! =', factorial(6))
    print(factorial.__name__)

# 上述例子有一个缺点: 遮盖了被装饰函数的__name__和__doc__属性。
# 输出：
# **************************************** Calling factorial(6)
# [0.00000093s] factorial(1) -> 1
# [0.00004992s] factorial(2) -> 2
# [0.00006112s] factorial(3) -> 6
# [0.00006905s] factorial(4) -> 24
# [0.00007791s] factorial(5) -> 120
# [0.00008724s] factorial(6) -> 720
# 6! = 720
# clocked
