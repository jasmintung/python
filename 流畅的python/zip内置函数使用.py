print(zip(range(3), 'ABC'))  # 返回一个生成器<zip object at 0x0000023382237088>
print(list(zip(range(3), 'ABC')))  # 构建列表[(0, 'A'), (1, 'B'), (2, 'C')]
print(list(zip(range(3), 'ABC', [0.0, 1.1, 2.2, 3.3])))  # [(0, 'A', 0.0), (1, 'B', 1.1), (2, 'C', 2.2)]
