import gevent


def fun1():
    print("A fuck B")
    gevent.sleep(2)
    print("A fuck back B")


def fun2():
    print("A fuck C")
    gevent.sleep(1)
    print("A fuck back C")


def fun3():
    print("B fuck D")
    gevent.sleep(1)
    print("B fuck back D")


def fun4():
    print("E fuck F")
    gevent.sleep(4)
    print("E fuck back F")

gevent.joinall([gevent.spawn(fun1),
                gevent.spawn(fun2),
                gevent.spawn(fun3),
                gevent.spawn(fun4)])

