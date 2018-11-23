def average():
    total = 0.0  # 因为协程的原因,只需要声明为局部变量
    count = 0
    average = None
    while True:
        term = yield average
        total += term
        count += 1
        average = total/count


coro_avg = average()
next(coro_avg)  # 预激活协程
print(coro_avg.send(10))  # 10.0
print(coro_avg.send(30))  # 20.0
print(coro_avg.send(5))  # 15.0
