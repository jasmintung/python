from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from usdb import models
from django.forms.models import model_to_dict
import json
import datetime
# Create your views here.


def login(request):
    """
    登陆验证
    :param request:
    :return:
    """
    print("fsdfsdaf")
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
            group_list = models.WorkGroup.objects.all()  # 获取分组信息传递给注册界面用
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
                return redirect(reverse('manage'))
                # return redirect('/usdb/manage/?' + "loginname" + "=" + name)
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


def manage(request):
    """
    管理员主界面
    :param request:
    :param username:
    :return:
    """
    print("manage")
    if request.method == "GET":
        return render(request, 'manage.html')  # 进入到管理主界面


def addgroup(request):
    """
    添加组
    :param request:
    :return:
    """
    print("addgroup")
    ret = {'statues': True, 'error': None, 'data': None}
    groupname = request.POST.get('g_name', None)
    group_type = request.POST.get('i_choicegroup', None)
    print("groupname:", groupname)
    try:
        # print(models.WorkGroup.objects.filter(caption=groupname).first())
        if group_type == '1':
            if models.WorkGroup.objects.filter(caption=groupname).first() is None:
                print("create group")
                models.WorkGroup.objects.create(caption=groupname)
                # g_obj = models.WorkGroup.objects.create(caption=groupname)
                # print(g_obj)
                ret['error'] = '添加成功'
            else:
                ret['statues'] = False
                ret['error'] = '组名已被使用'
        elif group_type == '2':
            if models.InterestGroups.objects.filter(name=groupname).first() is None:
                print("create interest group")
                models.InterestGroups.objects.create(name=groupname)
                # g_obj = models.WorkGroup.objects.create(caption=groupname)
                # print(g_obj)
                ret['error'] = '添加成功'
            else:
                ret['statues'] = False
                ret['error'] = '组名已被使用'

    except Exception as ex:
        ret['status'] = False
        ret['error'] = ex
    return HttpResponse(json.dumps(ret))
    # result = ""
    # if g_obj:
    #     result = "添加成功"
    # else:
    #     result = "添加失败"
    # # result = "添加成功"
    # return render(request, 'manage.html', {'operate_result': result})  # 进入到管理主界面


# def getgroupinfo(request, type):
#     """
#     获取组信息
#     :param request:
#     :return:
#     """
#     print("获取用户组信息:", type)
#     login_info = {}
#     login_info['type'] = 2
#     g_list = models.WorkGroup.objects.all()
#     print(g_list)
#     if type == '1':
#         # 修改组信息时
#         return render(request, 'manage.html', {'title_info': "用户组信息", 'hide': "cancelhide", 'group_list': g_list, 'operation': "ok"})
#     elif type == '2':
#         # 添加用户获取组信息时
#         return render(request, 'manage.html', {'loginInfo': login_info, 'group_list': g_list, 'hide': "cancelhide_adusr"})


def getgroupinfo(request, type):
    """
    获取组信息
    :param request:
    :return:
    """
    print("获取用户组信息:")
    g_list = models.WorkGroup.objects.all()
    ig_list = models.InterestGroups.objects.all()
    print(g_list)
    if type == 1:
        return render(request, 'manage.html', {'title_info': "用户组信息", 'hide': "cancelhide",
                                               'group_list': g_list, 'igroup_list': ig_list, 'operation': "ok"})
    elif type == 2:
        return render(request, 'manage.html', {'title_info': "增加用户", 'group_list': g_list, 'igroup_list': ig_list, 'hide': "cancelhide_adusr"})


def modifygroup(request):
    """
    修改组信息
    :param request:
    :return:
    """
    ret = {'statues': True, 'error': "修改成功", 'data': None}
    if request.method == "POST":
        # print(request.POST.lists)
        info = {}

        for key in request.POST.lists():
            info = json.loads(key[0])  # 字符串转为字典
        print("info = :", info)
        # print(type(info))
        work_group_list = info.get('g_list')
        interest_group_list = info.get('ig_list')
        for index in range(len(work_group_list)):
            for k, v in work_group_list[index].items():
                print(type(k))  # 字符串类型的ID
                print(k, v)
                obj = models.WorkGroup.objects.filter(gid=int(k)).update(caption=v)
                if obj:
                    pass
                else:
                    ret['statues'] = False
                    ret['error'] = "修改失败"

        for index in range(len(interest_group_list)):
            for k, v in interest_group_list[index].items():
                print(k, v)
                obj = models.InterestGroups.objects.filter(id=int(k)).update(name=v)
                if obj:
                    pass
                else:
                    ret['statues'] = False
                    ret['error'] = "修改失败"
    # return render(request, 'manage.html', {'operate_type': 1, 'operate_result': result})  # 进入到管理主界面
    # return redirect()
    return HttpResponse(json.dumps(ret))


def addusers(request):
    """
    添加员工信息
    :param request:
    :return:
    """
    user_list = []
    interest_group = []
    user_info = {}
    add_number = 0
    result = 1
    operate_obj = None
    # print(request.POST.getlist)
    ret = {'statues': True, 'error': "添加成功", 'data': None}
    if request.method == "POST":
        for key in request.POST.lists():
            # print(key[0])  # 获取到列表
            user_list = json.loads(key[0])
        for index in range(len(user_list)):
            print(user_list[index])
            print("111:", user_list[index].get('username'))
            print("222:", user_list[index].get('i_group'))
            print("333:", user_list[index].get('level'))
            models.UserInfo.objects.create(username=user_list[index].get('username'),
                                           password=user_list[index].get('password'),
                                           email=user_list[index].get('email'),
                                           phone=user_list[index].get('phone'),
                                           user_type_id=int(user_list[index].get('level')),
                                           user_group_id=int(user_list[index].get('w_group')))  # 注意这里user_group_id这个必须这样写代表的是user_group的uid!!!
            interest_group = user_list[index].get('i_group')
            new_user = (models.UserInfo.objects.filter(username=user_list[index].get('username')).values('uid'))
            for line in new_user:
                print(line)
                print(type(line))  # 字典
                for i in range(len(interest_group)):
                    print(interest_group[i])
                    obj = models.InterestGroups.objects.filter(id=interest_group[i]).first()
                    obj.r.add(line.get('uid'))
        # return render(request, 'manage.html', {'operate_result': result})  # 进入到管理主界面
        # return render(request, 'manage.html', {'operate_type': 2, 'operate_result': result})  # 进入到管理主界面
    return HttpResponse(json.dumps(ret))


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
    ret = {'statues': True, 'error': None, 'data': None}
    try:
        if models.WorkGroup.objects.filter(gid=gid).delete() is None:
            ret['statues'] = False
            ret['error'] = "删除失败"
        else:
            ret['statues'] = True
            ret['error'] = "删除成功"
            ret['data'] = gid
    except Exception as ex:
        ret['statues'] = False
        ret['error'] = "删除失败"
    return HttpResponse(json.dumps(ret))


def deluser(request, uid):
    """
    删除用户
    :param request:
    :param uid:
    :return:
    """
    ret = {'statues': True, 'error': None, 'data': None}
    print("delete user")
    print(uid)
    try:
        if models.UserInfo.objects.filter(uid=uid).delete() is None:
            ret['statues'] = False
            ret['error'] = "删除失败"
        else:
            ret['statues'] = True
            ret['error'] = "删除成功"
            ret['data'] = uid
    except Exception as ex:
        ret['statues'] = False
        ret['error'] = "删除失败"
    # return render(request, 'manage.html', {'operate_type': 4, 'operate_result': result})  # 进入到管理主界面
    return HttpResponse(json.dumps(ret))


def userdetailinfo(request, uid):
    """
    获取用户详细信息
    :param request:
    :param uid:
    :return:
    """
    obj = None
    result = 1
    user_list = []
    i_group_list = []
    w_group = {}
    wgroup_name = ""
    wgroup_id = 0
    ret = {'statues': True, 'error': None, 'data': None}
    try:
        obj = models.UserInfo.objects.all().values("uid", "username", "password", "phone", "email",
                                                   "user_type_id").filter(uid=uid)
        wgroup_name = models.UserInfo.objects.filter(uid=uid)[0].user_group.caption
        wgroup_id = models.UserInfo.objects.filter(uid=uid)[0].user_group.gid
        w_group[wgroup_id] = wgroup_name
        for line in obj:
            #######################
            # 多对多查询,看官方文档即可
            try:
                m2mobj = models.UserInfo.objects.get(uid=uid).interestgroups_set.all()
                # 遍历每个对象
                for m2mline in m2mobj:
                    group_info = {}
                    print(m2mline.name, m2mline.id)
                    group_info[m2mline.id] = m2mline.name
                    i_group_list.append(group_info)
                    print(i_group_list)
            except Exception as ex:
                print(ex)
            line['i_group'] = i_group_list
            line['w_group'] = w_group
            user_list.append(line)
            #######################
        ret['data'] = user_list
    except Exception as ex:
        print(ex)
        ret['statues'] = False
        ret['error'] = ex
    print("return detail")
    print(ret)
    # return render(request, 'manage.html', {'operate_type': 5, 'operate_result': result, 'u_detail': obj})  # 进入到管理主界面
    return HttpResponse(json.dumps(ret))


def modifyuser(request, uid):
    """
    获取要修改的用户资料
    :param request:
    :param uid:
    :return:
    """
    print("modifyuser: ", uid)
    ret = {'statues': True, 'error': None, 'data': None}
    need_modify_info = []
    w_group_list = []
    i_group_list = []
    i_selected_group_list = []

    try:
        obj = models.UserInfo.objects.all().values("uid", "username", "password", "phone", "email",
                                                   "user_type_id", "user_group").filter(uid=uid)
        wgroupsinfo = models.WorkGroup.objects.all().values("gid", "caption")
        print("可选工作组信息:", wgroupsinfo)
        for line in wgroupsinfo:
            w_group_list.append(line)
        igroupsinfo = models.InterestGroups.objects.all().values("id", "name")
        print("可选兴趣组信息:", igroupsinfo)
        for line in igroupsinfo:
            i_group_list.append(line)
        for line in obj:
            try:
                m2mobj = models.UserInfo.objects.get(uid=uid).interestgroups_set.all()
                for m2mline in m2mobj:
                    group_info = {}
                    # print(m2mline.name, m2mline.id)
                    group_info[m2mline.id] = m2mline.name
                    i_selected_group_list.append(group_info)
                    # print(i_group_list)
            except Exception as ex:
                ret['statues'] = False
                ret['error'] = ex
            line['select_wgroup'] = w_group_list  # 可选工作组信息
            line['select_igroup'] = i_group_list  # 可选兴趣组信息
            line['selected_igroup'] = i_selected_group_list  # 已经选择的兴趣组信息
            print("已选兴趣组信息:", i_selected_group_list)
            need_modify_info.append(line)
        ret['data'] = need_modify_info
    except Exception as ex:
        ret['statues'] = False
        ret['error'] = ex
    # return ruserinfoender(request, 'manage.html', {'operate_type': 6, 'operate_result': result,
    #                                        'u_obj': userinfo, 'g_obj': groupinfo})
    # print(ret)
    return HttpResponse(json.dumps(ret))


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
