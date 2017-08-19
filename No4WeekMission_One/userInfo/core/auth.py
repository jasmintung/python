import json
import getpass
import os

fileDst = os.path.dirname(os.path.dirname(os.path.abspath("__file__")))+"\db\\accounts"


def auth_process():
    while True:
        # print(os.path.abspath(__file__))
        # print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        str1 = "select  * from staff_table where dept = \"IT\""
        str2 = str1.split("where")
        print(str2)
        if str2[0].startswith("select") and len(str2) > 1:  # has where clause
            column, val = str2[1].strip().split("=") # 去掉字符串头尾的空字符,以=号进行分割
            print(column, val) # 得到键值,这个用法很神奇
        print("*******登陆*********")
        userName = input("用户名: ")
        print("是否显示密码? y / n")
        choice = input("输入 :")
        if choice == 'y' or choice == 'Y':
            password = input("密码: ")
        elif choice == 'n' or choice == 'N':
            password = getpass.getpass("密码: ")
        else:
            continue
        # 登陆验证
        # 从文件里面找到读取用户名,密码,个人记载的登陆次数,三个字段信息
        with open(fileDst, 'r', encoding='utf-8') as f:
            file_length = os.path.getsize(fileDst)
            if file_length > 0:
                loadDict = json.load(f)    # JSON转换成DICT字典
                # print(loadDict)
                if loadDict.get(userName) is None:
                    print("账户未注册!")
                else:
                    # print(loadDict.get(userName))
                    L = loadDict.get(userName)
                    urn = userName
                    pwd = L[0]    # 密码
                    count = int(L[1])    # 登陆失败记录次数
                    if count >= 3:
                        print("您的账户已被锁定!")
                        count = 0
                    else:
                        if urn == userName and password == pwd:
                            print("登陆成功")
                            # 将当前账户登陆失败次数清零写入文件记录
                            loadDict.get(userName)[1] = 0
                            # 将当前账户登陆失败次数清零写入文件记录
                            with open(fileDst, 'w', encoding='utf-8') as f:
                                json.dump(loadDict, f)
                                f.flush()    # 将缓存数据实时刷入文件
                            break
                        else:
                            if password != pwd:
                                if urn == userName:
                                    print("用户名或者密码错误!")
                                    count += 1
                                    # 将当前账户登陆失败次数写入文件JSON记录
                                    loadDict.get(userName)[1] = count
                                    with open(fileDst, 'w', encoding='utf-8') as f:
                                        json.dump(loadDict, f)
                                        f.flush()
            else:
                print("账户未注册!")