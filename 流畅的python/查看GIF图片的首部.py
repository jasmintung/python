import struct

fmt = '<3s3sHH'  # 小字节序列，两个3字节序列，两个16位二进制整数
with open('timg.gif', 'rb') as fp:
    img = memoryview(fp.read())
header = img[:10]
print(bytes(header))  # b'GIF89a\xc2\x01F\x01'
print(struct.unpack(fmt, header))  # (b'GIF', b'89a', 450, 326) 类型, 版本，宽度和高度
del header  # 删除引用,释放memoryview实例所占的内存
del img
