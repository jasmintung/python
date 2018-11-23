## 为了清楚说明可迭代的对象和迭代器之间的重要区别,详细介绍请看有道云笔记“可迭代对象与迭代器的对比”
import re
import reprlib

RE_WORD = re.compile('\w+')


class Sentence:

    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)  # 字符串列表

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        return SentenceIterator(self.words)  # 返回一个迭代器


class SentenceIterator:

    def __init__(self, words):
        self.words = words
        self.index = 0

    def __next__(self):
        try:
            word = self.words[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return word  # 返回单词

    def __iter__(self):
        return self


s3 = Sentence('Pig and Pepper')
it = iter(s3)
print(it)  # <__main__.SentenceIterator object at 0x000002682787FA20>
print(next(it))
print(next(it))
print(next(it))
# print(next(it))
print(list(it))  # []
print(list(iter(s3)))  # ['Pig', 'and', 'Pepper']
