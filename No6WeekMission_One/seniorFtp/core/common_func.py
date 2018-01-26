import random


def auth_code(self):
    """
    生成验证码
    :return: 返回验证码
    """
    checkcode = ""
    for i in range(4):
        current = random.randrange(0, 4)
        if current == i:
            temp = chr(random.randint(65, 90))  # ASCII码转成字符
        else:
            temp = random.randint(0, 9)
        checkcode += str(temp)
    return checkcode
