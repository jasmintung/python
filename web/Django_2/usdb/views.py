from django.shortcuts import render, redirect, HttpResponse
from usdb import models
import datetime
# Create your views here.


def login(request):
    """
    登陆验证
    :param request:
    :return:
    """
    if request.method == "GET":
        print("GET:")
        return render(request, 'login.html')
    elif request.method == "POST":
        print("POST")
        error_msg = ""
        obj_all = None
        obj_name = None
        login_info = {}
        name = request.POST.get('n_usr', None)
        password = request.POST.get('n_pwd', None)
        isWillToRg = request.POST.get('rgbtn', None)
        # print(request.POST)
        u_type = request.POST.get('u_type', None)  # 登陆角色: 1用户,2管理员
        print("role type:", u_type)
        if isWillToRg:
            group_list = models.UserGroup.objects.all()  # 获取分组信息传递给注册界面用
            # group_list = [{'uid':1, 'caption':"前端组"}, {'uid':2, 'caption':"项目实施组"}] 测试用
            return render(request, 'register.html', {'group_list': group_list})
        else:
            print(name, password)
            if u_type == '1':
                obj_all = models.UserInfo.objects.filter(username=name, password=password)
                obj_name = models.UserInfo.objects.filter(username=name).first()
            elif u_type == '2':
                # print("+++++++++++++++++++++++++")
                # print(models.adminInfo.objects.all())
                # print("+++++++++++++++++++++++++")
                obj_all = models.adminInfo.objects.filter(username=name, password=password)
                obj_name = models.adminInfo.objects.filter(username=name).first()
            # print("obj_all:", obj_all)
            # print("obj_name:", obj_name)
            if obj_all:
                login_info['type'] = int(u_type)
                login_info['name'] = name
                return render(request, 'manage.html', {'loginInfo': login_info})  # 进入到管理主界面
            else:
                if obj_name:
                    error_msg = "密码错误!"
                else:
                    error_msg = "用户不存在!"
                return render(request, 'login.html', {'error_msg': error_msg})


def registe(request):
    """
    注册
    :param request:
    :return:
    """
    warninginfo = ""
    print(request.POST)
    name = request.POST.get('username', None)
    email = request.POST.get('email', None)
    phone = request.POST.get('phone', None)
    password = request.POST.get('password', None)
    u_type = request.POST.get('u_type', None)
    group_id = request.POST.get('group_id', None)
    obj_name = models.UserInfo.objects.filter(username=name).first()
    print(name, email, phone, password, u_type, group_id)
    if obj_name:
        warninginfo = "用户名已存在"
        return render(request, 'register.html', {'warning_info': warninginfo})
    else:
        obj = models.UserInfo.objects.create(username=name, password=password, email=email,
                                                phone=phone, user_type_id=u_type, user_group=group_id)
        if obj:
            return HttpResponse("注册成功")
        else:
            return HttpResponse("注册失败")


def addgroup(request):
    """
    添加组
    :param request:
    :return:
    """
    groupname = request.POST.get('g_name', None)
    print("groupname:", groupname)
    g_obj = models.UserGroup.objects.create(caption=groupname)
    result = ""
    if g_obj:
        result = "添加成功"
    else:
        result = "添加失败"
    # result = "添加成功"
    return render(request, 'manage.html', {'operate_result': result})  # 进入到管理主界面


def getgroupinfo(request, type):
    """
    获取组信息
    :param request:
    :return:
    """
    print("获取用户组信息:", type)
    login_info = {}
    login_info['type'] = 2
    g_list = models.UserGroup.objects.all()
    print(g_list)
    if type == '1':
        # 修改组信息时
        return render(request, 'manage.html', {'title_info': "用户组信息", 'hide': "cancelhide", 'group_list': g_list, 'operation': "ok"})
    elif type == '2':
        # 添加用户获取组信息时
        return render(request, 'manage.html', {'loginInfo': login_info, 'group_list': g_list, 'hide': "cancelhide_adusr"})


def modifygroup(request):
    """
    修改组信息
    :param request:
    :return:
    """
    result = 1  # 1表示成功
    if request.method == "POST":
        print(request.POST.lists)
        for key in request.POST.lists():  # 这里是获取的格式类似这样:('1', ['技术支持'])
            print(key)  # ('1', ['技术支持'])
            gid = int(key[0])
            # print(type(id))
            name = "".join('%s' % ix for ix in key[1])
            # print(type(name))
            # print(gid, name)
            obj = models.UserGroup.objects.filter(uid=gid).update(caption=name)
            if obj:
                pass
            else:
                result = 0
    return render(request, 'manage.html', {'operate_type': 1, 'operate_result': result})  # 进入到管理主界面


def addusers(request):
    """
    添加员工信息
    :param request:
    :return:
    """
    user_info = {}
    add_number = 0
    result = 1
    operate_obj = None
    if request.method == "POST":
        # print(request.POST.lists)
        for key in request.POST.lists():  # 这里是获取的格式类似这样:('1', ['技术支持'])
            user_info[key[0]] = key[1]
        add_number = len(user_info.get('username'))
        print(add_number)
        for row in range(add_number):
            operate_obj = models.UserInfo.objects.create(username=user_info.get('username')[row],
                                                         password=user_info.get('pwd')[row],
                                                         email=user_info.get('email')[row],
                                                         phone=user_info.get('phone')[row],
                                                         user_type_id=int(user_info.get('choicelevel')[row]),
                                                         user_group_id=int(user_info.get('choicegroup')[row])) # 注意这里user_group_id这个必须这样写代表的是user_group的uid!!!
            if operate_obj is None:
                result = 0
                return render(request, 'manage.html', {'operate_result': result})  # 进入到管理主界面
        return render(request, 'manage.html', {'operate_type': 2, 'operate_result': result})  # 进入到管理主界面


def getuserinfo(request):
    """
    用户信息
    :param request:
    :return:
    """
    u_list = models.UserInfo.objects.all()
    return render(request, 'manage.html', {'title_info': "用户信息", 'hide': "canceluserhide", 'user_list': u_list})


def delgroup(request, gid):
    """
    删除组
    :param request:
    :param gid:
    :return:
    """
    result = 1
    try:
        models.UserGroup.objects.filter(uid=gid).delete()
    except Exception as ex:
        result = 0
    return render(request, 'manage.html', {'operate_type': 3, 'operate_result': result})  # 进入到管理主界面


def deluser(request, uid):
    """
    删除用户
    :param request:
    :param uid:
    :return:
    """
    result = 1
    try:
        models.UserInfo.objects.filter(id=uid).delete()
    except Exception as ex:
        result = 0
    return render(request, 'manage.html', {'operate_type': 4, 'operate_result': result})  # 进入到管理主界面


def userdetailinfo(request, uid):
    """
    获取用户详细信息
    :param request:
    :param uid:
    :return:
    """
    obj = None
    result = 1
    try:
        obj = models.UserInfo.objects.filter(id=uid).first()
    except Exception as ex:
        print(ex)
        result = 0
    print("return detail")
    return render(request, 'manage.html', {'operate_type': 5, 'operate_result': result, 'u_detail': obj})  # 进入到管理主界面


def modifyuser(request, uid):
    """
    获取要修改的用户资料
    :param request:
    :param uid:
    :return:
    """
    print("modifyuser")
    result = 1
    userinfo = None
    groupinfo = None
    try:
        userinfo = models.UserInfo.objects.filter(id=uid).first()
        groupinfo = models.UserGroup.objects.all()
    except Exception as ex:
        print(ex)
        result = 0
    print(groupinfo)
    return render(request, 'manage.html', {'operate_type': 6, 'operate_result': result,
                                           'u_obj': userinfo, 'g_obj': groupinfo})


def modifyuser_up(request, uid):
    """
    提交修改的用户资料
    :param request:
    :param uid:
    :return:
    """
    print(uid)
    print(request.POST)
    result = 1
    try:
        models.UserInfo.objects.filter(id=uid).update(password=request.POST.get('pwd'),
                                                      email=request.POST.get('email'),
                                                      phone=request.POST.get('phone'),
                                                      user_type_id=int(request.POST.get('m_choicelevel')),
                                                      user_group=int(request.POST.get('m_choicegroup')))
    except Exception as ex:
        print(ex)
        result = 0
    return render(request, 'manage.html', {'operate_type': 7, 'operate_result': result})
