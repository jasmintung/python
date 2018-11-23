import sys
import re

WORD_RE = re.compile(r'\w+')

index = {}
print(sys.argv[1])
with open(sys.argv[1], encoding='utf-8') as fp:
    for line_no, line in enumerate(fp, 1):
        # line_no:文件行号, line: 每一行的内容
        for match in WORD_RE.finditer(line):  # #由于返回的为MatchObject的iterator，所以我们需要迭代并通过MatchObject的方法输出
            word = match.group()
            column_no = match.start() + 1
            location = (line_no, column_no)
            occurrences = index.get(word, [])  # 第一次key查询
            occurrences.append(location)
            index[word] = occurrences  # 第二次key查询
    for word in sorted(index, key=str.upper):
        print(word, index[word])


# 使用setdefault进行优化
print("优化后")
with open(sys.argv[1], encoding='utf-8') as fp:
    for line_no, line in enumerate(fp, 1):
        # line_no:文件行号, line: 每一行的内容
        for match in WORD_RE.finditer(line):  # #由于返回的为MatchObject的iterator，所以我们需要迭代并通过MatchObject的方法输出
            word = match.group()
            column_no = match.start() + 1
            location = (line_no, column_no)
            # occurrences = index.get(word, [])  # 第一次key查询
            # occurrences.append(location)
            # index[word] = occurrences  # 第二次key查询
            index.setdefault(word, []).append(location)  # 一次key查询
    for word in sorted(index, key=str.upper):
        print(word, index[word])


print("再次优化后")


import collections

index = collections.defaultdict(list)  # 把list构造方法作为default_factory来创建一个defaultdict
with open(sys.argv[1], encoding='utf-8') as fp:
    for line_no, line in enumerate(fp, 1):
        # line_no:文件行号, line: 每一行的内容
        for match in WORD_RE.finditer(line):  # #由于返回的为MatchObject的iterator，所以我们需要迭代并通过MatchObject的方法输出
            word = match.group()
            column_no = match.start() + 1
            location = (line_no, column_no)
            index[word].append(location)  # word不存在,default_factory会被调用,为查询不到的键创造一个值,这个值是一个空的列表被赋值给index[word]
    for word in sorted(index, key=str.upper):
        print(word, index[word])
