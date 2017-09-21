import json, time, os
from conf import settings

conn_params = settings.DATABASE
db_path = "%s/%s" % (conn_params["path"], conn_params["name"]) # 数据库绝对路径
db_path_bak = db_path + ".tmp"


def file_db_handle(conn_params):
    """
    parse the db file path
    :param conn_params: the db connections params set in setttings
    :return:
    """
    print("file db:", conn_params)
    return file_excute


def db_handler():
    """
    connect to db
    :param conn_parms: the db connection params set in setttings
    :return: a
    """

    conn_params = settings.BASE_DB # 获得数据库的地址(这里就是employinfo_storage)
    return file_db_handle(conn_params)
    # if conn_params['engine'] == 'file_storage':
    #         return file_db_handle(conn_params)
    #     elif conn_params['engine'] == 'mysql':
    #         pass


def file_excute(sql, **kwargs):
    """
    数据库核心操作
        select name,age from staff_table where age > 22
　　     select  * from staff_table where dept = "IT"
        select  * from staff_table where enroll_date like "2013"
        delete *from staff_table where 列名称 = 值
    :param sql: 解析sql语句 "select * from XXX where starffId=%s" % starffId
    :param kwargs:
    :return:
    """

    print(sql, db_path)
    if sql.find("where") >= 0:
        sql_list = sql.split("where") # 将sql语句以where关键字进行拆分为两个元素
        print(sql_list)
        if sql_list[0].startswith("select") and len(sql_list) > 1:
            if sql_list[1].strip().find(">") != -1:
                column1, val1 = sql_list[1].strip().split(">")  # 分解
                search_core(1, column1, val1)
            elif sql_list[1].strip().find("<") != -1:
                column2, val2 = sql_list[1].strip().split("<")  # 分解
                search_core(2, column2, val2)
            elif sql_list[1].strip().find("=") != -1:
                column3, val3 = sql_list[1].strip().split("=")  # 分解
                search_core(3, column3, val3)
            elif sql_list[1].strip().find("like") != -1:
                column4, val4 = sql_list[1].strip().split("like")  # 分解
                search_core(4, column4, val4)
            else:
                print("not support this operation")
        elif sql_list[0].startswith("update") and len(sql_list) > 1:
            column0 = sql_list[0].split("=")
            dst_value = column0[1]
            column1, source_val = sql_list[1].strip().split("=")
            update_core(column1.strip(), source_val.strip(), dst_value.strip())  # 更新的字段类型, 更新前数据, 更新后数据
        elif sql_list[0].startswith("delete") and len(sql_list) > 1:
            column0, val = sql_list[1].strip().split("=") # 分解
            delete_core(column0.strip(), val.lstrip())

    else:
        if sql.startswith("insert") and len(sql) > 1:
            sql_list = sql.split("=")
            add_core(sql_list[1].lstrip())


def delete_core(*args):
    """
    删除处理核心逻辑
    :param args:属性+值
    :return:
    """
    print(args)

    if os.path.isfile(db_path):
        with open(db_path, "r") as rf, \
             open(db_path_bak, "w") as wf:
            for epinfo in rf:
                tmp_dict = eval(epinfo)
                if args[0] == "starffId" or args[0] == "age":
                    if tmp_dict.get(args[0]) == int(args[1]):
                        print("delete success!")
                    else:
                        wf.writelines(str(tmp_dict)+'\n')
                else:
                    if tmp_dict.get(args[0]) == args[1]:
                        print("delete success!")
                    else:
                        wf.writelines(str(tmp_dict)+'\n')
        os.remove(db_path)
        os.rename(db_path_bak, db_path)


def add_core(args):
    """
    添加处理核心逻辑
    :param args:
    :return:处理结果
    """
    print(args)

    if os.path.isfile(db_path):
        with open(db_path, "a") as af:
            af.writelines(str(args)+'\n')
            print("增加完成!")
    else:
        print("is not file")


def update_core(*args):
    """
    更新处理核心逻辑
    :param args:
    :return:处理结果
    """
    print(args)
    modify = False
    if os.path.isfile(db_path):
        with open(db_path, "r") as rf, \
             open(db_path_bak, "w") as wf:
                for epinfo in rf:
                    tmp_dict = eval(epinfo)  # 将字符串转换成字典
                    if tmp_dict.get(args[0]) == args[1]:
                        tmp_dict[args[0]] = args[2]
                        modify = True
                        print("修改成功")
                    wf.writelines(str(tmp_dict)+'\n')
        os.remove(db_path)
        os.rename(db_path_bak, db_path)
    else:
        print("is not file")
    if modify is False:
        print("修改失败")

# 后面搜索算法可进行优化


def search_core(do_type, *args):
    """
    查询处理核心逻辑
    :param do_type:选择按哪种方式搜索
    :param args: 搜索属性,搜索条件
    :return:
    """
    do_type = int(do_type)

    colum = args[0].strip()  # 搜索属性
    val = args[1].strip()  # 搜索条件
    print(colum, val)

    if do_type == 1:  # 支持年龄,ID的搜索
        if os.path.isfile(db_path):
            with open(db_path, "r") as rf:
                for epinfo in rf:
                    # print(epinfo.strip('\n'))  # 打印并过滤每一行末尾的\n
                    tmp_dict = eval(epinfo)  # 将字符串转字典
                    # print(type(tmp_dict))
                    if colum == "starffId":  # 根据员工ID来删选
                        if tmp_dict.get("starffId") > int(val):
                            print("符号条件的员工ID是: ", tmp_dict.get("starffId"))
                    elif colum == "age":  # 根据员工年龄
                        if tmp_dict.get("age") > int(val):
                            print("符号条件的员工年龄有: ", tmp_dict.get("age"))
                    else:
                        print("not support this operation")
    elif do_type == 2:  # 支持年龄, ID的搜索
        if os.path.isfile(db_path):
            with open(db_path, "r") as rf:
                for epinfo in rf:
                    # print(epinfo.strip('\n'))
                    tmp_dict = eval(epinfo)
                    # print(type(tmp_dict))
                    if colum == "starffId":
                        if tmp_dict.get("starffId") < int(val):
                            print("符号条件的员工ID是: ", tmp_dict.get("starffId"))
                    elif colum == "age":  # 根据员工年龄
                        if tmp_dict.get("age") < int(val):
                            print("符号条件的员工年龄有: ", tmp_dict.get("age"))
                    else:
                        print("not support this operation")
    elif do_type == 3:  # 支持按部门查找
        print("按照部门查找")
        if os.path.isfile(db_path):
            with open(db_path, "r") as rf:
                for epinfo in rf:
                    # print(epinfo.strip('\n'))
                    tmp_dict = eval(epinfo)
                    # print(type(tmp_dict))
                    if colum == "dept":
                        if tmp_dict.get("dept") == val:
                            print("符合条件的员工ID是: %d 部门是 %s" % (tmp_dict.get("starffId"), tmp_dict.get("dept")))
                    else:
                        print("not support this operation")
    elif do_type == 4:  # 模糊查找(支持英文姓名, 修改日期)
        print("模糊查找")
        if os.path.isfile(db_path):
            with open(db_path, "r") as rf:
                for epinfo in rf:
                    # print(epinfo.strip('\n'))
                    tmp_dict = eval(epinfo)
                    # print(type(tmp_dict))
                    if colum == "name":
                        if tmp_dict.get("name").find(val) != -1:
                            print("符号条件的员工ID是: ", tmp_dict.get("starffId"))
                    elif colum == "enroll date":
                        if tmp_dict.get("enroll date").find(val) != -1:
                            print("符合条件的员工ID是: ", tmp_dict.get("starffId"))
                    else:
                        print("not support this operation")

        else:
            exit("\033[31;1m not exist!\033[0m")

