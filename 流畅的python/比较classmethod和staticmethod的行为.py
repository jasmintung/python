class Demo:
    @classmethod
    def klassmeth(*args):
        return args

    @staticmethod
    def statmeth(*args):
        return args


print(Demo.klassmeth())  # (<class '__main__.Demo'>,)
print(Demo.klassmeth('spam'))  # (<class '__main__.Demo'>, 'spam')
print(Demo.statmeth())  # ()
print(Demo.statmeth('spam'))  # ('spam',)
