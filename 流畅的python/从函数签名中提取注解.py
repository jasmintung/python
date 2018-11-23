from inspect import signature


def clip(text:str, max_len:'int > 0'=80) ->str:
    """
    在max_len前面或后面的第一个空格处截断文本
    :param text:
    :param max_len:
    :return:
    """
    pass


sig = signature(clip)
print(sig.return_annotation)
for param in sig.parameters.values():
    note = repr(param.annotation).ljust(13)  # 将对象转化为供解释器读取的形式(字符串),并左对齐
    print(note, ':', param.name, '=', param.default)
