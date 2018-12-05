# ts_dict = {'name': 'zhangtong', 'age': 28}
# for key in ts_dict:
#     print(key, ts_dict[key])
#
#
# import array
#
# array_list = array.array('l', )
# print(array_list[1])

test_list = [1, 2, 3, 4, 5]
ms = ",".join('%s' % cmd for cmd in test_list)
print(ms)

list_1 = {"name":"", "age": ""}
tuple_1 = ["zhangtong", 30]
final = zip(list_1, tuple_1)
print(type(final))
for key in final:
    print(key)
