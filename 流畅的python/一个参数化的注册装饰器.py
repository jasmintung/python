registry = set()


def register(active=True):
    def decorate(func):
        print('running register(active=%s)->decorate(%s)' % (active, func))
        if active:
            registry.add(func)
        else:
            registry.discard(func)
        return func
    return decorate


@register(active=False)
def f1():
    print('running f1()')


@register()
def f2():
    print('running f2()')


def f3():
    print('running f3()')

# 这里直接运行结果输出:
# running register(active=False)->decorate(<function f1 at 0x000001929608D268>)
# running register(active=True)->decorate(<function f2 at 0x000001929608D2F0>)


print(registry)  # {<function f2 at 0x00000154B08CD2F0>}
register()(f3)  # running register(active=True)->decorate(<function f3 at 0x0000020FC8BDD1E0>)
print(registry)  # {<function f3 at 0x0000018EB5D2D1E0>, <function f2 at 0x0000018EB5D2D2F0>}
register(active=False)(f2)  # running register(active=False)->decorate(<function f2 at 0x00000250162AD378>)
print(registry)  # {<function f3 at 0x000002563BF1D1E0>}


