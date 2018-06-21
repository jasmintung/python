# -*-coding:utf-8-*-
import sys


print(sys.getdefaultencoding())

name = "你好"
print(name)  # 打印：你好
print(name.encode("gbk"))  # 打印：b'\xc4\xe3\xba\xc3'
name = "Alex"


def change_name():
    name = "Alex2"

    def change_name2():
        name = "Alex3"
        print("第3层打印", name)

    change_name2()  # 调用内层函数
    print("第2层打印", name)


change_name()
print("最外层打印", name)

it = iter([1, 2, 3, 4, 5])

while True:
    try:
        x = next(it)
        print(x)
    except StopIteration:
        break

for i in [1, 2, 3, 4, 5]:
    print(i)
