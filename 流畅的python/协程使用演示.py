def simple_coroutine():
    print('-> coroutine started')
    x = yield
    print('-> coroutine recevied:', x)


my_coro = simple_coroutine()
print(my_coro)  # <generator object simple_coroutine at 0x00000253BB474A40>
print(next(my_coro))  # -> coroutine started
my_coro.send(42)
# None
# -> coroutine recevied: 42
