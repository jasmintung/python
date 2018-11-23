class C:
    pass


def func():
    pass


print(func.__name__)
obj = C()
print(sorted(set(dir(func)) - set(dir(obj))))  # 计算差集
# ['__annotations__', '__call__', '__closure__', '__code__', '__defaults__', '__get__',
# '__globals__', '__kwdefaults__', '__name__', '__qualname__']