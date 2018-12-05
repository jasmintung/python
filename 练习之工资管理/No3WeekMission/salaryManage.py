import os
fileDist = "C:\\Users\jasmintung\PycharmProjects\HomePractice\salaymanagement\info.txt"
fileDistBak = "C:\\Users\jasmintung\PycharmProjects\HomePractice\salaymanagement\infobak.txt"


def search():
    """查询员工工资"""
    with open(fileDist, 'a', encoding="utf-8") as af:
        if os.path.getsize(fileDist) == 0:
            print("没有员工记录!")
        else:
            name = input("请输入要查询的员工姓名")
            search_check(name)


def search_check(arg):
    """公用查询模块"""
    with open(fileDist, 'a+', encoding="utf-8") as af:
        af.seek(0)
        if os.path.getsize(fileDist) > 0:
            if arg.isalpha():
                for personInfo in af:
                    if arg in personInfo:
                        print("%s的工资是: %s " %(arg, int(personInfo.lstrip(arg))))
                        return True
            else:
                index = arg.find(" ")
                if len(arg) - index < 2 or arg.count(" ") > 1:
                    print("输入格式不对")
                else:
                    if arg.find(" "):
                        print("输入格式正确!")
                        return search_check(arg[0:index])
                    else:
                        print("输入格式不对")
                        return False
    print("没有这个人！")
    return False


def modify():
    """修改员工工资"""
    modifyinfo = input("请输入要修改的员工姓名和工资，用空格分隔（例如：Alex 10）:")
    if modifyinfo.isalpha() or modifyinfo.isalnum():
        pass
    else:
        if search_check(modifyinfo):
            with open(fileDist, 'r', encoding="utf-8") as rf, \
                 open(fileDistBak, 'w', encoding="utf-8") as wf:
                for personInfo in rf:
                    if modifyinfo[0:modifyinfo.index(" ")] in personInfo:
                        personInfo = personInfo.replace(personInfo, modifyinfo + '\n')
                    wf.writelines(personInfo)
            os.remove(fileDist)
            os.rename(fileDistBak, fileDist)
            # os.remove(fileDistBak)
            print("修改成功")
        else:
            print("修改失败")


def add():
    """增加新员工记录"""
    addinfo = input("请输入要增加的员工姓名和工资，用空格分割（例如：Eric 100000）")
    if addinfo.isalpha() or addinfo.isalnum():
        pass
    else:
        if search_check(addinfo):
            print("已存在此员工!")
        else:
            with open(fileDist, 'a', encoding="utf-8") as af:
                if os.path.getsize(fileDist) > 0:
                    af.writelines('\n' + addinfo)
                else:
                    af.writelines(addinfo)
                print("增加成功!")


def process_choice(arg):
    """处理用户选项"""
    if arg.isdigit():
        if int(arg) == 1:
            search()
        elif int(arg) == 2:
            modify()
        elif int(arg) == 3:
            add()
            pass
        elif int(arg) == 4:
            return 0
        else:
            print("没有这个选项!")
    else:
        print("非法输入!")
print("******工资管理系统******")
while True:
    print("1. 查询员工工资")
    print("2. 修改员工工资")
    print("3. 增加新员工记录")
    print("4. 退出")
    choice = input("请选择:")
    if process_choice(choice) == 0:
        print("再见!")
        break