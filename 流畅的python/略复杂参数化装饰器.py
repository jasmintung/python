import time


DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'


def clock(fmt=DEFAULT_FMT):  # 参数话装饰器工厂函数
    def decorate(func):  # 真正的装饰器
        def clocked(*_args):  # 包装被装饰的函数
            t0 = time.time()
            _result = func(*_args)
            elapsed = time.time() - t0
            name = func.__name__
            args = ', '.join(repr(arg) for arg in _args)
            result = repr(_result)  # 对象转字符串
            print(fmt.format(**locals()))  # 引用clocked的局部变量
            return _result
        return clocked
    return decorate


if __name__ == '__main__':
    @clock()
    def snooze(seconds):
        time.sleep(seconds)

    for i in range(3):
        snooze(.123)

