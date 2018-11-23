import collections
from random import choice
# namedtuple用户构建只有少数属性没有方法的对象,比如数据库条目
Card = collections.namedtuple('Card', ['rank', 'suit'])


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                       for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]


beer_card = Card('7', 'diamonds')
print(beer_card)  # Card(rank='7', suit='diamonds')
deck = FrenchDeck()
print(deck)
print(len(deck))  # 52
for i in range(len(deck)):  # 可迭代
    print(deck[i])  # Card对象的实例

# 随机抽取
print(choice(deck))
print("11111")
print(choice(deck))
print("22222")
print(choice(deck))
print("33333")

# 因为__getitem__把[]操作i交给了self._card列表，所以deck对象自动支持切片操作,细思确实是
print(deck[:3])  # 打印出0~2的值
print(deck[12::13])

# in运算符可用在FrenchDeck类上,因为它是可迭代的
print(Card('Q', 'hearts') in deck)  # True
print(Card('7', 'beasts') in deck)  # False

# 总结: 对合成的运用使得__len__和__getitem__的具体实现可以代理给self._cards这个Python列表
