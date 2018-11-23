import time
import functools


def clock(func):
    @functools.wraps(func)  # 把相关属性从func拷贝到clocked
    def clocked(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - t0
        name = func.__name__
        arg_lst = []
        if args:
            arg_lst.append(', '.join(repr(arg) for arg in args))
        if kwargs:
            pairs = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
            arg_lst.append(pairs)
        arg_str = ', '.join(arg_lst)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result
    return clocked


@clock
def factorial(n):
    return 1 if n < 2 else n * factorial(n - 1)

if __name__ == '__main__':
    print(factorial.__name__)  # factorial
