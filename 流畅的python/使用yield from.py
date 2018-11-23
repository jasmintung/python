def gen():
    for c in 'AB':
        yield c
    for i in range(1, 3):
        yield i


print(list(gen()))  # ['A', 'B', 1, 2]

# 改用yield from


def gen_yf():
    yield from 'AB'
    yield from range(1, 3)


print(list(gen_yf()))  # ['A', 'B', 1, 2]
