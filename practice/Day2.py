intab = "aeiou"  # This is the string having actual characters.
outtab = "98765"  # This is the string having corresponding mapping character
trantab = str.maketrans(intab, outtab)

str = "this is string example....wow!!!"
print(str.translate(trantab))
msg = "my name is{}, and age is{}"
print(msg.partition('is'))
print(msg.swapcase())
print(msg.zfill(40))
b = "ddeefafaf_哈哈"
print(b.isidentifier())  # 判断是否符合命名规则
