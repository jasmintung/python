def chain(*iterables):
    for it in iterables:
        yield from it


s = 'ABC'
t = tuple(range(3))
print(t)  # (0, 1, 2)
print(list(chain(s, t)))  # ['A', 'B', 'C', 0, 1, 2]

# 说明: yield from x 对x对象做的第一件事是, 调用iter(x),从中获取迭代器。因此x 可以是任何迭代的对象
# yield from的主要功能是打开双向通道, 把最外层的调用方与最内层的子生成器连接起来,这样二者可以直接发送和产出值,还可以直接传入异常,
# 而不用在位于中间的协程中添加大量处理异常的样板代码。有了这个结构, 协程可以通过以前不可能的方式委托在职责
