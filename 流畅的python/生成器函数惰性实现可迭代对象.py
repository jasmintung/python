# re.finditer函数是re.findall函数的惰性版本,返回的不是列表,而是一个生成器，按需生成re.MatchObject实例。
# 如果有很多匹配, re.finditer函数能节省大量内存!!
import re
import reprlib


RE_WORD = re.compile('\w+')


class Sentence:

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        for match in RE_WORD.finditer(self.text):
            yield match.group()

