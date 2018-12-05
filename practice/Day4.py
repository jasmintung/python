# a = [i+1 for i in range(10)]
# print(a)
# b = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# c = map(lambda x:x+1, b)
# for i in c:
#     print(i)
# d = (j+1 for j in range(10))
# print(d)
# print(next(d))
# print(next(d))
#
# import time
# def consumer(name):
#     print("%s 准备吃包子啦!" %name)
#     while True:
#        baozi = yield
#
#        print("包子[%s]来了,被[%s]吃了!" %(baozi,name))
#
#
# def producer(name):
#     c = consumer('A')
#     c2 = consumer('B')
#     c.__next__()
#     c2.__next__()
#     print("老子开始准备做包子啦!")
#     for i in range(10):
#         time.sleep(1)
#         print("做了2个包子!")
#         c.send(i)
#         c2.send(i)
#
# producer("alex")

b = [i for i in range(10)]
print(b)  # 列表推导生成一个列表[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
c = [i for i in range(10, -1, -1)]  # [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
print(c)
d = [i for i in range(10) if i % 2 == 0 and i != 0]  # [2, 4, 6, 8]
print(d)
e = [1, 2, 3, 4, 5, 6, 7, 8, 9]
f = map(lambda x: x+1, e)
print(f)
for i in f:
    print(i, end=' ')  # 2 3 4 5 6 7 8 9 10


# 列表生成式取完值后列表生成式对象里没有值了,这个过程时不可逆的
g = (x for x in range(10))
print(g)
for i in g:
    print(i)
    # print(next(g))
# 0 1 2 3 4 5 6 7 8 9
# 后面的循环没有值可取了:
for i in g:
    print("fdas:", i)

# yield模拟并发

import time


def consumer(args):
    print("args is ready")
    while True:
        things = yield
        print("{} consumer: {}".format(args, things))


def produce():
    c1 = consumer('A')
    c2 = consumer('B')
    c1.__next__()
    c2.__next__()
    for i in range(10):
        time.sleep(0.5)
        c1.send(i)
        c2.send(i)


produce()
