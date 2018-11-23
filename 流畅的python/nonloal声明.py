def make_averager():
    count = 0
    total = 0

    def averager(new_value):
        nonlocal count, total  # 因为编译器编译时会把它们当作是局部变量,但找不到绑定值所以会出错,所以加上nonlocal声明它们是自由变量
        count += 1
        total += new_value
        return total / count
    return averager


avg = make_averager()
print(avg(10))
print(avg(11))
