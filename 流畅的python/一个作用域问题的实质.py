b = 6
t_list = []


def f2(a):
    global b  # 没有这句声明,程序会报错
    print(a)
    print(b)
    print(t_list)
    b = 9
    t_list.extend([1, 2, 3])
    print(t_list)


f2(3)
