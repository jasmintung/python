import re
import reprlib


RE_WORD = re.compile('\w+')


class Sentence:

    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        for word in self.words:
            yield word  # 这个迭代器是生成器对象,每次调用__iter__方法会自动创建，自动返回,生成完全部值后直接退出
        return  # 不是必要的


# 完成,不要再单独定义迭代器类!!!
s3 = Sentence('Pig and Pepper')
print(s3) # Sentence('Pig and Pepper')
it = iter(s3)
print(it)  # <__main__.SentenceIterator object at 0x000002682787FA20>
print(next(it))
print(next(it))
print(next(it))
# print(next(it))
print(list(it))  # []
print(list(iter(s3)))  # ['Pig', 'and', 'Pepper']
