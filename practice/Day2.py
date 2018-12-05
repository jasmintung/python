intab = "aeiou"  # This is the string having actual characters.
outtab = "98765"  # This is the string having corresponding mapping character
trantab = str.maketrans(intab, outtab)

str = "this is string example....wow!!!"
print(str.translate(trantab))
msg = "my name is{}, and age is{}"
print(msg.partition('is')) # 以is为分段将字符串切成三段组成元祖('my name ', 'is', '{}, and age is{}')
print(msg.swapcase())  # 大小写转换MY NAME IS{} AND AGE IS{}
print(msg.zfill(40))  # 右对齐左边补零 000000000000000my name is{} and age is{}
b = "ddeefafaf_哈哈"
print(b.isidentifier())  # 判断是否符合命名规则

s1 = [1,2,3]
s2 = [4,5,6]
print(s1 + s2)
# intab = "aeiou"
# outtab = "12345"
# transtab = str.maketrans(intab, outtab)
#
# strs = "this is a string example...wow!!!"
# print(strs.translate(transtab))  # th3s 3s 1 str3ng 2x1mpl2...w4w!!!
#
# msg = "my name is{} and age is{}"
# print(msg.partition('is'))
# print(msg.swapcase())
# print(msg.zfill(40))
# bts = "$efafa_哈哈"
# print(bts.isidentifier())  # False
# s1 = [1, 2, 3]
# s2 = [4, 5, 6]
# print(s1 + s2)  # 列表组合 [1, 2, 3, 4, 5, 6]
