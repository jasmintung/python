# __author__:"Tony Cheung"

import re

bracket = re.compile(r'\([^()]+\)')  # 寻找最内层括号规则
mul = re.compile(r'(\d+\.?\d*\*-\d+\.?\d*)|(\d+\.?\d*\*\d+\.?\d*)')  # 寻找乘法运算规则
div = re.compile(r'(\d+\.?\d*/-\d+\.?\d*)|(\d+\.?\d*/\d+\.?\d*)')  # 寻找除法运算规则
add = re.compile(r'(-?\d+\.?\d*\+-\d+\.?\d*)|(-?\d+\.?\d*\+\d+\.?\d*)')  # 寻找加法运算规则
sub = re.compile(r'(-?\d+\.?\d*--\d+\.?\d*)|(-?\d+\.?\d*-\d+\.?\d*)')  # 寻找减法运算规则
c_f = re.compile(r'\(?\+?-?\d+\)?')  # 检查括号内是否运算完毕规则
strip = re.compile(r'[^(].*[^)]')  # 去掉括号规则


def Mul(s):
    """计算表达式中的乘法运算"""
    exp = re.split(r'\*', mul.search(s).group())
    return s.replace(mul.search(s).group(), str(float(exp[0]) * float(exp[1])))


def Div(s):
    """计算表达式中的除法运算"""
    exp = re.split(r'/', div.search(s).group())
    return s.replace(div.search(s).group(), str(float(exp[0]) / float(exp[1])))


def Add(s):
    """计算表达式中的加法运算"""
    exp = re.split(r'\+', add.search(s).group())
    return s.replace(add.search(s).group(), str(float(exp[0]) + float(exp[1])))


def Sub(s):
    """计算表达式中的减法运算"""
    exp = sub.search(s).group()
    if exp.startswith('-'):
        exp = exp.replace('-', '+')
        res = Add(exp).replace('+', '-')
    else:
        exp = re.split(r'-', exp)
        res = str(float(exp[0]) - float(exp[1]))
    return s.replace(sub.search(s).group(), res)


def calc():
    """程序入口"""
    while True:
        note = input("请输入算式 (q: 退出):")
        check_left_kuohao = re.findall(r"\)*\)", note)
        str_l_kuohao = ''.join(check_left_kuohao)  # 列表转字符串计算括号数量
        check_right_kuohao = re.findall(r"\(*\(", note)
        str_r_kuohao = ''.join(check_right_kuohao)  # 列表转字符串计算括号数量
        if len(str_l_kuohao) != len(str_r_kuohao):
            print("括号没配对!!!")
            continue
        if note == 'q':
            break
        else:
            note = ''.join([x for x in re.split('\s+', note)])  # 去掉空格重组
            if not note.startswith('('):  # 若用户输入的表达式首尾无括号,则统一格式化为:(表达式)
                note = str('(%s)' % note)
            while bracket.search(note):  # 若表达式note存在括号
                note = note.replace('--', '+')  # 检查表达式,并将--运算替换为+运算
                note_search = bracket.search(note).group()  # 得到最内层括号及其内容赋给变量note_search
                if div.search(note_search):
                    note = note.replace(note_search, Div(note_search))
                elif mul.search(note_search):
                    note = note.replace(note_search, Mul(note_search))
                elif sub.search(note_search):
                    note = note.replace(note_search, Sub(note_search))
                elif add.search(note_search):
                    note = note.replace(note_search, Add(note_search))
                elif c_f.search(note_search):  # 检查括号内运算是否完毕
                    note = note.replace(note_search, strip.search(note_search).group())  # 将括号去掉
            print("计算结果: %.2f" % (float(note)))

if __name__ == '__main__':
    calc()
