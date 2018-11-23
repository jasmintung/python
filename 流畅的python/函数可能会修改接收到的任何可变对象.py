def f(a, b):
    a += b
    return a


x = 1
y = 2
print(f(x, y))  # 3
a = [1, 2]
b = [3, 4]
print(f(a, b))  # [1, 2, 3, 4]
print(a)  # [1, 2, 3, 4]
print(b)  # [3, 4]
t = (10, 20)
u = (30, 40)
print(f(t, u))  # (10, 20, 30, 40)
print(t)  # (10, 20)
print(u)  # (30, 40)
