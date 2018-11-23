import random


class BingoCage:
    def __init__(self, items):
        self._items = list(items)
        print(self._items)  # [0, 1, 2]
        random.shuffle(self._items)  # 把列表里元素的位置打乱

    def pick(self):
        try:
            return self._items.pop()  # 取出一个元素
        except IndexError:
            raise LookupError('pick from empty BingoCage')

    def __call__(self, *args, **kwargs):
        return self.pick()


bingo = BingoCage(range(3))
print(bingo.pick())
print(bingo())
print(callable(bingo))  # True
print(dir(len))