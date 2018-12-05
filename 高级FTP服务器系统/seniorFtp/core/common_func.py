import random
import time
import sys
# 说明：UTF兼容ISO8859-1和ASCII，GB18030兼容GBK，GBK兼容GB2312，GB2312兼容ASCII
CODES = ["utf-8", "gbk", "gb2312", "ASCII", "Unicode"]
# UTF-8 BOM前缀字节
UTF_8_BOM = b'\xef\xbb\xbf'


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


# 获取文件编码类型
def file_encoding(file_path):
    """
    获取文件编码类型\n
    :param file_path: 文件路径\n
    :return: \n
    """
    with open(file_path, 'rb') as f:
        return string_encoding(f.read())


        # 获取字符编码类型


def string_encoding(b: bytes):
    """
    获取字符编码类型\n
    :param b: 字节数据\n
    :return: \n
    """
    # 遍历编码类型
    for code in CODES:
        try:
            b.decode(encoding=code)
            if 'utf-8' == code and b.startswith(UTF_8_BOM):
                return 'utf-8'
            else:
                return code
        except Exception:
            continue
    return '未知的字符编码类型'


def progress_bar(section, all, current, total):
    """
    进度条打印
    :param section:当前文件的段号
    :param all: 文件总共分段数
    :param current: 已经计算的值
    :param total: 总计值
    :return:
    """
    # while current != total:
    # sys.stdout.write('\r')
    # sys.stdout.write("暂停:%s%%[%s][%s]" % (int(current * 100 / total), section, all))
    sys.stdout.write('\r')
    sys.stdout.write("进度:%s%%[%s][%s]" % (int(current*100 / total), section, all))
    sys.stdout.flush()
    time.sleep(0.5)
    if current == total:
        sys.stdout.write('\n')
