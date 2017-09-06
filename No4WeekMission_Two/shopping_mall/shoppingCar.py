import os
import json
import getpass
import datetime
import os
import sys
consumerBarcode = 1141880000    # 交易单号每一笔必须不一致,涉及到字典的操作,从文件读取
purcharsedgoods = []
goods = []
dictAccount = {}
choiceNum = 0
userName = None
retryGoodNumber = False
base_dir = os.path.dirname(os.path.abspath(__file__))
userfileDst = "%s\%s" % (base_dir, "users.txt")
recordFileDst = "%s\%s" % (base_dir, "buyRecords.txt")
goodsFileDst = "%s\%s" % (base_dir, "goods.txt")
accountFileDst = "%s\%s" % (base_dir, "accountManager.txt")
consumerBarcodeFileDst = "%s\%s" % (base_dir, "consumerBarcode.txt")
root_path = "%s/atm" % os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_path)
print(root_path)
# from atm.bin import atm
# atm.atm_entry_test()  # 能够调用ATM模块的函数测试打印
from core import main


def login_func(user_name, passwd):
    """登陆验证,从文件里面找到读取用户名,密码,个人记载的登陆次数,失败超过3次,锁定账户"""
    login_statue = False    # 登陆状态
    with open(userfileDst, 'r', encoding='utf-8') as f:
        load_dict = json.load(f)  # JSON转换成
        # print(loadDict)
        if load_dict.get(user_name) is None:
            print("账户未注册!")
        else:
            # print(loadDict.get(user_name))
            list_user_info = load_dict.get(user_name)
            urn = user_name
            pwd = list_user_info[0]  # 密码
            login_count = int(list_user_info[1])  # 登陆失败记录次数
            if login_count >= 3:
                login_count = 0
                login_statue = False
                print("您的账户已被锁定!")
            else:
                if urn == userName and passwd == pwd:
                    print("登陆成功")
                    # 将当前账户登陆失败次数清零写入文件记录
                    load_dict.get(user_name)[1] = 0
                    with open(userfileDst, 'w', encoding='utf-8') as f:
                        json.dump(load_dict, f)
                        f.flush()  # 将缓存数据实时刷入文件
                    login_statue = True
                else:
                    if passwd != pwd:
                        if urn == user_name:
                            print("用户名或者密码错误!")
                            login_count += 1
                            # 将当前账户登陆失败次数写入文件JSON记录
                            load_dict.get(user_name)[1] = login_count
                            with open(userfileDst, 'w', encoding='utf-8') as f:
                                json.dump(load_dict, f)
                                f.flush()
    return login_statue


def account_check():
    """对当前登陆用户进行账户检查,没有存钱的提示存钱"""
    balance = 0  # 账户余额
    is_update = False
    account_info = {}
    with open(accountFileDst, 'r', encoding="utf-8") as af:
        file_length = os.path.getsize(accountFileDst)
        if file_length > 0:
            account_info = json.load(af)
            if userName not in account_info:
                is_update = True
            else:
                print("您当前的余额是: ")
                balance = account_info.get(userName).get("余额")
                print(balance)
        else:
            is_update = True
    if is_update is True:
        print("您的账户还没有存钱.")
        deposit = int(input("请输入存放的金额: "))
        account = {"余额": deposit}
        account_info[userName] = account
        balance = deposit
        with open(accountFileDst, 'w+', encoding="utf-8") as wacf:
            wacf.writelines(json.dumps(account_info, ensure_ascii=False))  # 转为json格式存入文件
    return balance


def account_settle(args):
    """本次购买支付结算处理"""
    # 更新个人资产
    if args == "C":
        with open(accountFileDst, 'r', encoding="utf-8") as acrf:
            account_info = json.load(acrf)
        with open(accountFileDst, 'w', encoding='utf-8') as acuf:
            account_info.get(userName)["余额"] = customer_cash
            acuf.write(json.dumps(account_info, ensure_ascii=False))
    elif args == "CDC":
        # 这里调用ATM模块的接口进行信用卡消费
        if main.run(100) is not True:
            print("支付失败!")
            return

    record_dict = {}
    with open(recordFileDst, 'r', encoding='utf-8') as rcf:
        record_file_len = os.path.getsize(recordFileDst)
        if record_file_len > 0:
            record_dict = json.load(rcf)
    shop_car_list = {}
    record_load_dict = {}

    # 将本次交易记录写入文件
    with open(consumerBarcodeFileDst, 'r', encoding="utf-8") as cbdf:
        file_size = os.path.getsize(consumerBarcodeFileDst)
        if file_size == 0:
            file_size = consumerBarcode
        else:
            serial_no = cbdf.read()
            serial_no = int(serial_no)
            serial_no += 1
            file_size = serial_no
    with open(consumerBarcodeFileDst, 'w+', encoding="utf-8") as cbdf:
        cbdf.write(str(file_size))
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    shop_car_list["消费时间"] = str(now)
    for m in range(len(purcharsedgoods)):
        n = 0
        if m % 3 == 0:
            n = m + 1
            buy_things = [purcharsedgoods[n + 1], purcharsedgoods[n]]
            shop_car_list[purcharsedgoods[m]] = buy_things
    if len(record_dict) == 0:
        record_load_dict[file_size] = shop_car_list
        record_dict[userName] = record_load_dict
    else:
        if record_dict.get(userName) is None:  # 还没有当前客户的消费记录
            record_load_dict[file_size] = shop_car_list
            record_dict[userName] = record_load_dict
        else:
            record_dict[userName][file_size] = shop_car_list
    print(record_dict)
    with open(recordFileDst, 'w', encoding='utf-8') as wf, \
            open(goodsFileDst, 'w', encoding='utf-8') as gdf:
        # 更新购买记录
        wf.write(json.dumps(record_dict, ensure_ascii=False))
        wf.flush()
        # 更新商品库存
        gdf.write(json.dumps(goods, ensure_ascii=False))
        gdf.flush()

    print("支付成功!")
    print("欢迎再次光临!")
    purcharsedgoods.clear()


def shopping_receipt_show():
    print("------------------------------")
    print("购物总计:")
    print("\t名称:\t\t单价*数量\t\t\t小计")
    for m in range(len(purcharsedgoods)):
        n = 0
        if m % 3 == 0:
            n = m + 1
            print("\t\t%s\t\t" % (purcharsedgoods[m]), purcharsedgoods[n], end='')
            print("*", end='')
            print(purcharsedgoods[n + 1], end='')
            print("\t\t\t", purcharsedgoods[n] * purcharsedgoods[n + 1])
    print("------------------------------")
    print("您的现金余额是: %d RMB" % customer_cash)
    print("请输入: 继续选购(B), 现金结算(C),信用卡支付(CDC),放弃退出(Q)")

while True:
    print("**********欢迎**********")
    loginRole = input("普通用户请输入: 1\n管理员请输入: 2\n退出请输入: 0\n--->")
    if loginRole.isdigit():
        loginRole = int(loginRole)    # 必须要类型转换,输入的默认类型是字符串
        if loginRole == 1:
            userName = input("用户名: ")
            print("是否显示密码? y / n")
            choice = input("输入 :")
            if choice == 'y' or choice == 'Y':
                password = input("密码: ")
            elif choice == 'n' or choice == 'N':
                password = getpass.getpass("密码: ")
            else:
                continue
            if login_func(userName, password) is True:
                customer_cash = account_check()
                with open(goodsFileDst, 'r', encoding='utf-8') as gf:
                    goods = json.load(gf)
                while True:
                    for i in range(len(goods)):
                        if i % 2 == 0:
                            j = i
                            print("编号: ", goods[i])
                            print("%s:单价 %.2f 库存 %d" % (goods[j+1][0], goods[j+1][1], goods[j+1][2]))
                    print("请根据编号选择商品,退出输入Q")
                    choiceNo = input()
                    if choiceNo == 'Q':
                        print("欢迎再次光临!")
                        break
                    else:
                        if choiceNo.isdigit():
                            choiceNo = int(choiceNo)
                            if choiceNo in goods:
                                print("请输入购买数量,0表示清空购物车对应的商品,退出输入Q")
                                choiceNum = input()
                                if choiceNum.isdigit():
                                    retryGoodNumber = True
                                    if ((int(choiceNum) > int(goods[goods.index(choiceNo) + 1][2]))
                                            or (int(goods[goods.index(choiceNo) + 1][2]) == 0)):
                                        print("库存不够!")
                                        retryGoodNumber = False
                                        break
                                    else:
                                        getNumber = 0  # 实际可购买的商品数量
                                        if len(purcharsedgoods) != 0:
                                            for k in range(len(purcharsedgoods)):
                                                if k % 3 == 0:
                                                    if purcharsedgoods[k] == goods[goods.index(choiceNo) + 1][0]:
                                                        print("购物车已存在的商品")
                                                        # 购物车里已经有相同的商品,则余额需要先加上购物车里面的消费总额再减去本次消费总额
                                                        # 本商品信息数量也是需要先加上购物车里的总数再减去本次消费的总数
                                                        # 这样做的目的就是兼顾了增删改三个功能
                                                        customer_cash += purcharsedgoods[
                                                                             k + 2] * \
                                                                         goods[goods.index(choiceNo) + 1][1]
                                                        goods[goods.index(choiceNo) + 1][2] += purcharsedgoods[
                                                            k + 2]
                                                        if int(choiceNum) == 0:    # 从购物车删除这项商品
                                                            print("您不要 %s 了" % purcharsedgoods[k])
                                                            del purcharsedgoods[k:k+3]
                                                        else:
                                                            for i in range(int(choiceNum)):
                                                                if customer_cash >= goods[goods.index(choiceNo) + 1][1]:
                                                                    customer_cash -= goods[goods.index(choiceNo) + 1][1]
                                                                else:
                                                                    print("您的余额不够了!")
                                                                    break
                                                                getNumber += 1
                                                            if getNumber > 0:
                                                                # print("增加%d个" % getNumber)
                                                                purcharsedgoods[k + 2] = getNumber
                                                                goods[goods.index(choiceNo) + 1][2] -= getNumber
                                                        break
                                                else:  # 购物车车里还没有这个商品哦
                                                    if k == len(purcharsedgoods) - 1:
                                                        if int(choiceNum) == 0:
                                                            pass
                                                        else:
                                                            print("购物车还无此商品")
                                                            for i in range(int(choiceNum)):
                                                                if customer_cash >= goods[goods.index(choiceNo) + 1][1]:
                                                                    customer_cash -= goods[goods.index(choiceNo) + 1][1]
                                                                else:
                                                                    print("您的余额不够!")
                                                                    break
                                                                getNumber += 1
                                                            # print("增加%d个" % getNumber)
                                                            if getNumber > 0:
                                                                purcharsedgoods.append(
                                                                    goods[goods.index(choiceNo) + 1][0])  # 商品名称
                                                                purcharsedgoods.append(
                                                                    goods[goods.index(choiceNo) + 1][1])  # 商品单价
                                                                purcharsedgoods.append(getNumber)
                                                                goods[goods.index(choiceNo) + 1][2] -= getNumber
                                        else:  # 购物车还是空的
                                            if int(choiceNum) == 0:
                                                retryGoodNumber = False
                                                print("非法输入!")
                                            else:
                                                for i in range(int(choiceNum)):
                                                    if customer_cash >= goods[goods.index(choiceNo) + 1][1]:
                                                        customer_cash -= goods[goods.index(choiceNo) + 1][1]
                                                    else:
                                                        print("您的余额不够!")
                                                        break
                                                    getNumber += 1
                                                if getNumber == 0:
                                                    retryGoodNumber = False
                                                elif getNumber > 0:
                                                    print("新增加%d个" % getNumber)
                                                    purcharsedgoods.append(goods[goods.index(choiceNo) + 1][0])  # 商品名称
                                                    purcharsedgoods.append(goods[goods.index(choiceNo) + 1][1])  # 商品单价
                                                    purcharsedgoods.append(getNumber)
                                                    goods[goods.index(choiceNo) + 1][2] -= getNumber
                                else:
                                    if choiceNum == 'Q':
                                        retryGoodNumber = False
                                        break
                                    else:
                                        print("非法输入!")
                                        retryGoodNumber = False
                            else:
                                print("抱歉没有这个商品哦")
                        else:
                            print("输入有误重新输入!")
                            continue
                    if retryGoodNumber is True:
                        retryGoodNumber = False
                        print("是否继续选购？继续(Y),浏览购物车(P)")
                        continueChoice = input()
                        if continueChoice == "Y":
                            continue
                        elif continueChoice == 'P':
                            if len(purcharsedgoods) == 0:
                                print("您的购物车是空的!")
                                purcharsedgoods.clear()
                            else:
                                shopping_receipt_show()
                                continueChoice = input()
                                if continueChoice == "B":
                                    pass
                                elif continueChoice == "C" or continueChoice == "CDC":
                                    account_settle(continueChoice)
                                    break
                                elif continueChoice == "Q":
                                    print("欢迎再次光临!")
                                    purcharsedgoods.clear()
                                    break
                        else:
                            print("输入有误,退出！！")
                            break
        elif loginRole == 2:
            pass
        elif loginRole == 0:
            print("您已退出.")
            break
        else:
            print("输入有误")
            continue
