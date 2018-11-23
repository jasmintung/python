def factorial(n):
    return 1 if n < 2 else n * factorial(n - 1)


fact = factorial
print(list(map(fact, range(6))))  # [1, 1, 2, 6, 24, 120]
print([fact(n) for n in range(6)])  # [1, 1, 2, 6, 24, 120]
print(list(map(factorial, filter(lambda n: n % 2, range(6)))))  # [1, 6, 120]
print([factorial(n) for n in range(6) if n % 2])  # [1, 6, 120]

