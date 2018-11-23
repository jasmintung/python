def gen_123():
    yield 1
    yield 2
    yield 3


print(gen_123)  # <function gen_123 at 0x0000020CF1C13E18>是函数对象
print(gen_123())  # <generator object gen_123 at 0x0000020CF3844A40>返回一个生成器对象
for i in gen_123():  # 生成器是迭代器,会生成传给yield表达式的值。
    print(i)  # 1 2 3

g = gen_123()
print(next(g))  # 1
print(next(g))  # 2
print(next(g))  # 3

