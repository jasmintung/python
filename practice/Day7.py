# class Flight:
#     """类的属性演示"""
#     def __init__(self, name):
#         self.flight_name = name
#
#     def checking_status(self):
#         print("checking flight %s status " % self.flight_name)
#         return 1
#
#     @property
#     def flight_status(self):
#         status = self.checking_status()
#         if status == 0:
#             print("flight got canceled...")
#         elif status == 1:
#             print("flight is arrived")
#         elif status == 2:
#             print("flight has departured already...")
#         else:
#             print("cannot confirm the flight status...,please check later")
#
#     @flight_status.setter  # 修改
#     def flight_status(self, status):
#         status_dic = {0: "canceled", 1: "arrived", 2: "departured"}
#         print("\033[31;1mHas changed the flight status to\033[0m", status_dic.get(status))
#
#     @flight_status.deleter  # 删除
#     def flight_status(self):
#         print("status got removed...")
#
# f = Flight("CA1980");
# f.flight_status
# f.flight_status = 2
# del f.flight_status
# print(Flight.__doc__)  # 打印冒号里面的注释内容
# print(Flight.__module__)  # 表示当前操作的对象在哪个模块
# print(Flight.__class__)  # 表示当前操作的对象的类是什么
# print(Flight)
# 类的生成过程

#
# class MyType(type):
#
#     def __int__(self, what, bases=None, dict=None):
#         super(MyType, self).__init__(what, bases, dict)
#
#     def __call__(self, *args, **kwargs):
#         obj = self.__new__(self, *args, **kwargs)
#         self.__init__(obj)
#         print(MyType.__name__)
#
#
# class Foo(object):
#
#     __metaclass__ = MyType
#
#     def __init__(self, name):
#         self.name = name
#
#     def __new__(cls, *args, **kwargs):
#         return object.__new__(cls, *args, **kwargs)
#
# obj = Foo("zhangtong")

# class Foo(object):
#
#     def __int__(self):
#         self.name = 'zhangtong'
#
#     def func(self):
#         return 'func'
#
# obj = Foo()
# # 判断是否有成员(类属性,方法)
# print(hasattr(obj, 'name'))  # False
# print(hasattr(obj, 'func'))  # True
# # 获取成员
# # getattr(obj, 'name')
# getattr(obj, 'func')
# # 设置成员
# setattr(obj, 'age', 18)
# setattr(obj, 'show', (lambda x:x + 1 ,[y for y in range(10)]))
# print(getattr(obj, 'age'))  # 18
# print(getattr(obj, 'show'))  # (<function <lambda> at 0x00000000003E3E18>, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
# # 删除成员
# # delattr(obj, 'name')
# delattr(obj, 'func')


# class Foo(object):
#     def __init__(self):
#         self.name = 'zhangtong'
#
#     def func(self):
#         return 'func'
#
#
# obj = Foo()
# print(hasattr(obj, 'name'))  # True
# print(hasattr(obj, 'func'))  # True
# print(getattr(obj, 'name'))  # zhangtong
# print(getattr(obj, 'func'))  # <bound method Foo.func of <__main__.Foo object at 0x000001CA176971D0>>
# setattr(obj, 'age', 18)
# setattr(obj, 'show', (lambda x: x+1, [y for y in range(10)]))
# print(getattr(obj, 'show'))  # (<function <lambda> at 0x000001F27664C1E0>, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
# s = getattr(obj, 'show')
# print(s[1][0])  # 0

class Base(object):
    def fun_base(self):
        print("this is base fun")


def fun(self):
    print("this is fun")


c = type('Foo', (Base, ), {'fun': fun, 'a': 1})
c1 = c()
print(c)  # <class '__main__.Foo'>
print(c1)  # <__main__.Foo object at 0x0000020778E671D0>
print(type(c1))  # <class '__main__.Foo'>
c1.fun()  # this is fun
c1.fun_base()  # this is base fun
print(c1.a)  # 1

#  对type进行封装


class MyType(type):
    def __new__(cls, name, base, dic):
        return super(MyType, cls).__new__(cls, name, base, dic)


#  把一个函数变成type
def metacls_func(name, base, dic):
    return type(name, base, dic)


# class C(object):
#     def __new__(cls, *args, **kwargs):
#         print("__new__ called. args is", args, 'kwargs is', kwargs)
#         print("the type of cls is", type(cls), 'the cls is', cls)
#         c = super(C, cls).__new__(cls, *args, **kwargs)
#         print("the type of c is", type(c), 'the c is', c)
#         return c
#
#     def __init__(self, *args, **kwargs):
#         print("__init__ called. args is", *args, 'kwargs is', kwargs)
#         print("the type of self is", type(self), 'the self is', self)
#
#
# c1 = C(1, 2, a=3)
# print(c1)
# c2 = C(3, 4, b=4)
# print(c2)
# 这段代码说明：
#
# __new()__的作用：当调用c1 = C(1, 2, a=3)时，class语句会查找__metaclass__生成class C，之后__new()__被调用，通过调用父类的__new()__生成对象（super(C, cls).__new__(cls, *args, **kwargs)的返回值是一个Class C的一个对象，类型是class C）
# __init()__的作用：当__new()__返回一个对象之后，会继续调用__init()__进行对象的初始化过程。（如果__new()__没有返回一个对象，那么后续的__init()__也不会被调用）
# cls与self：二者分别是__new()__、__init()__的参数，从上面的代码可以看出，cls就是由metaclass type生成的class C，而self就是class C生成的对象，在两次调用中，这个对象分别就是c1 = C(1, 2, a=3) c2 = C(3, 4, b=4)生成的c1和c2（self和它们的地址是一致的）
# __new()__与__init()__的参数传递： 当调用对象生成语句c1 = C(1, 2, a=3)的时候，会携带不定参数(1, 2, a=3)，这些参数会分别被传递给__new()__与__init()__


# 单例模式

class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, *args, **kwargs):
        pass


s1 = Singleton()
s2 = Singleton()
print(s1)
print(s2)
print(s1 == s2)

