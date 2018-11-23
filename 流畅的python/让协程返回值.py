from collections import namedtuple


Result = namedtuple('Result', 'count average')


def average():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield  # 没有返回值(产出值)
        if term is None:
            print("跳出")
            break
        total += term
        count += 1
        average = total/count
    return Result(count, average)


coro_avg = average()
next(coro_avg)
print(coro_avg.send(10))
print(coro_avg.send(30))
print(coro_avg.send(6.5))
try:
    coro_avg.send(None)
except StopIteration as exc:
    result = exc.value
    print(result)

# None
# None
# None
# 跳出
# Result(count=3, average=15.5)
