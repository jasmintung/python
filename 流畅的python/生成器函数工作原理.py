def gen_123():
    yield 1
    yield 2
    yield 3


print(gen_123)  # <function gen_123 at 0x0000020CF1C13E18>
print(gen_123())  # <generator object gen_123 at 0x0000020CF3844A40>
for i in gen_123():
    print(i)  # 1 2 3

g = gen_123()
next(g)  # 1
next(g)
next(g)

