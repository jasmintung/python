class Flight:
    """类的属性演示"""
    def __init__(self, name):
        self.flight_name = name

    def checking_status(self):
        print("checking flight %s status " % self.flight_name)
        return 1

    @property
    def flight_status(self):
        status = self.checking_status()
        if status == 0:
            print("flight got canceled...")
        elif status == 1:
            print("flight is arrived")
        elif status == 2:
            print("flight has departured already...")
        else:
            print("cannot confirm the flight status...,please check later")

    @flight_status.setter  # 修改
    def flight_status(self, status):
        status_dic = {0: "canceled", 1: "arrived", 2: "departured"}
        print("\033[31;1mHas changed the flight status to\033[0m", status_dic.get(status))

    @flight_status.deleter  # 删除
    def flight_status(self):
        print("status got removed...")

f = Flight("CA1980");
f.flight_status
f.flight_status = 2
del f.flight_status
print(Flight.__doc__)  # 打印冒号里面的注释内容
print(Flight.__module__)  # 表示当前操作的对象在哪个模块
print(Flight.__class__)  # 表示当前操作的对象的类是什么
print(Flight)
# 类的生成过程


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
class Foo(object):

    def __int__(self):
        self.name = 'zhangtong'

    def func(self):
        return 'func'

obj = Foo()
# 判断是否有成员(类属性,方法)
print(hasattr(obj, 'name'))  # False
print(hasattr(obj, 'func'))  # True
# 获取成员
# getattr(obj, 'name')
getattr(obj, 'func')
# 设置成员
setattr(obj, 'age', 18)
setattr(obj, 'show', (lambda x:x + 1 ,[y for y in range(10)]))
print(getattr(obj, 'age'))  # 18
print(getattr(obj, 'show'))  # (<function <lambda> at 0x00000000003E3E18>, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
# 删除成员
# delattr(obj, 'name')
delattr(obj, 'func')
