# import gevent
#
#
# def task(pid):
#     gevent.sleep(0.5)
#     print("Task %s done" % pid)
#
#
# def synchronous():
#     for i in range(1, 10):
#         task(i)
#
#
# def asynchronous():
#     threads = [gevent.spawn(task, i) for i in range(10)]
#     gevent.joinall(threads)
#
# print('Synchronous:')
# synchronous()
#
# print('Asynchronous:')
# asynchronous()  # 运行的结果不是唯一的


def test(type, **kwargs):
    print(kwargs)
    print(kwargs.get('name'))
    print(kwargs.get('age'))
test(0, name='zhangtong', age=17)

da = 17
print(type(da))
