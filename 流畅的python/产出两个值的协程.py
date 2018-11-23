def simple_coro2(a):
    print('-> Started: a =', a)
    b = yield a
    print('-> Received: b =', b)
    c = yield a + b
    print('-> Received: c =', c)


my_coro2 = simple_coro2(14)
from inspect import getgeneratorstate
print(getgeneratorstate(my_coro2))  # GEN_CREATED
next(my_coro2)  # -> Started: a = 14  产出数值14,并且暂停,等待为b赋值
print(getgeneratorstate(my_coro2))  # GEN_SUSPENDED
my_coro2.send(28)  # -> Received: b = 28 : 把数值28发给暂停的协程, 产出数值42,并且暂停,等待为c赋值
my_coro2.send(99)  # -> Received: c = 99
