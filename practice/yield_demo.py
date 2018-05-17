import time
import queue


def consumer(name):
    print("ready eat food")
    while True:
        new_baozi = yield
        print("{0} eat food:{1}".format(name, new_baozi))


def product():
    con1.__next__()
    con2.__next__()
    n = 0
    while n < 5:
        n += 1
        con1.send(n)
        con2.send(n)
        time.sleep(1)

if __name__ == "__main__":
    con1 = consumer("zhangtong")
    con2 = consumer("lis")
    p = product()
