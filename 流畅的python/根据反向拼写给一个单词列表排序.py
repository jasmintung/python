def reverse(word):
    return word[::-1]


fruits = ['strawberry', 'fig', 'apple', 'cherry', 'respberry', 'banana']
print(reverse('testing'))  # gnitset
print(sorted(fruits, key=reverse))  # ['banana', 'apple', 'fig', 'respberry', 'strawberry', 'cherry']

