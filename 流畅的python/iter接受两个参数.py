from random import randint


def d6():
    return randint(1, 6)


d6_iter = iter(d6, 1)
print(d6_iter)
for roll in d6_iter:
    print(roll)


def f():
    def do_yield(n):
        print(n)
        yield n
    x = 0
    while True:
        x += 1
        # do_yield(x)
        yield from do_yield(x)  # 解决方法，上句代码替换成这句


f()  # 得到的是一个无限循环.
