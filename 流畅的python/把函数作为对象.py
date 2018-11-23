def factorial(n):
    """
    return n!
    :param n:
    :return:
    """
    return 1 if n < 2 else n * factorial(n - 1)


print(factorial(42))
print(factorial.__doc__)  # 说明的那段字符串,__doc__是函数对象众多属性的一个
print(type(factorial))  # <class 'function'>

fact = factorial
print(fact)  # <function factorial at 0x00000227E23F3E18>
print(fact(5))  # 120
map(factorial, range(11))
print(list(map(fact, range(11))))  # [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800]
# 函数式编程的特点之一就是使用高阶函数
