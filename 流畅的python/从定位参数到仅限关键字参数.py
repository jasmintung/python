def tag(name, *content, cls=None, **kwargs):
    print(name, end=''+' | ')
    print(content, end=''+' | ')
    print(cls, end=''+' | ')
    print(kwargs)


tag('br')  # br | () | None | {}
tag('p', 'hello')  # p | ('hello',) | None | {}
tag('p', 'hello', 'world')  # p | ('hello', 'world') | None | {}
tag('p', 'hello', id=33)  # p | ('hello',) | None | {'id': 33}
tag('p', 'hello', 'world', cls='sidebar')  # p | ('hello', 'world') | sidebar | {}
tag(content='testing', name='img')  # img | () | None | {'content': 'testing'}
my_tag = {'name': 'img', 'title': 'Sunset Boulevard', 'src': 'sunset.jpg', 'cls': 'framed'}
tag(**my_tag)  # img | () | framed | {'title': 'Sunset Boulevard', 'src': 'sunset.jpg'}

# 定义函数时若想指定仅限关键字参数，要把它们放到前面有 * 的参数后面。如果不想支持数量不定的定位参数，但是想支持仅限关键字参数，在签名中放一个 *。


def f(a, *, b):
    return a, b


print(f(1, b=2))  # (1, 2)
