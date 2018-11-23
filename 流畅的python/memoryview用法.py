# memoryview() 函数返回给定参数的内存查看对象(Momory view)。
# 所谓内存查看对象，是指对支持缓冲区协议的数据进行包装，在不需要复制对象基础上允许Python代码访问。
v = memoryview(bytearray('abcdefg', 'utf-8'))
print(v[1])
print(v[-1])
print(v[1:4])
print(v[1:4].tobytes())
