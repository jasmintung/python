

def gen_AB():
    print('start')
    yield 'A'  # 在for循环中第一次隐式调用next()函数
    print('continue')
    yield 'B'  # 在for循环中第二次隐式调用next()函数
    print('end.')


for c in gen_AB():  # 与g = iter(gen_AB())一样,用于获取生成器对象,然后每次迭代时调用next(g)
    print("*"*6)
    print('-->', c)


# start
# ******
# --> A  # 生成器函数定义体中的yield 'A'语句会生成值A,提供给for循环使用,而A会赋值给变量c，最终输出--> A
# continue
# ******
# --> B
# end.
