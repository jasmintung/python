a = [i+1 for i in range(10)]
print(a)
b = [1, 2, 3, 4, 5, 6, 7, 8, 9]
c = map(lambda x:x+1, b)
for i in c:
    print(i)
d = (j+1 for j in range(10))
print(d)
print(next(d))
print(next(d))

import time
def consumer(name):
    print("%s 准备吃包子啦!" %name)
    while True:
       baozi = yield

       print("包子[%s]来了,被[%s]吃了!" %(baozi,name))


def producer(name):
    c = consumer('A')
    c2 = consumer('B')
    c.__next__()
    c2.__next__()
    print("老子开始准备做包子啦!")
    for i in range(10):
        time.sleep(1)
        print("做了2个包子!")
        c.send(i)
        c2.send(i)

producer("alex")