from django.shortcuts import render, redirect, HttpResponse, render_to_response
from django.urls import reverse
from usdb import models
from forms import registe_form
from django.template import RequestContext
import time
from django.forms.models import model_to_dict
import json
from signals import handel_err_s
import datetime
# Create your views here.
from django.views.decorators.csrf import csrf_exempt, csrf_protect


def auth(type):
    """
    装饰器做账户验证用,针对只设置cookie
    :param type:
    :return:
    """
    def deco(func):
        def inner(request, *args, **kwargs):
            v = None
            if type == 0:  # 管理员验证
                v = request.COOKIES.get('admincookies')
            elif type == 1:  # 普通用户验证
                v = request.COOKIES.get('usercookies')
            if not v:
                time.sleep(2)
                # 没有cookie那就直接返回到登陆界面
                return redirect('/usdb/login')
            else:
                v = json.loads(v)
                print("cookie:", v)
            return func(request, *args, **kwargs)
        return inner
    return deco


def login(request):
    """
    登陆验证
    :param request:
    :return:
    """
    if request.method == "GET":
        print("GET:")
        print(request.META)
        print(request.META.get('HTTP_X_CSRFTOKEN', None))  # 获取request headers头信息,根据key
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
        # print("role type:", u_type)
        if isWillToRg:
            return redirect('/usdb/registe/')
        else:
            # print(name, password)
            if u_type == '1':
                obj_all = models.UserInfo.objects.filter(username=name, password=password)
                obj_name = models.UserInfo.objects.filter(username=name).first()
            elif u_type == '2':
                obj_all = models.adminInfo.objects.filter(username=name, password=password)
                obj_name = models.adminInfo.objects.filter(username=name).first()
            # print("obj_all:", obj_all)
            # print("obj_name:", obj_name)
            if obj_all:
                # res = None
                # name = json.dumps(name)  # 不这样转换的话cookie操作时会报错UnicodeEncodeError,针对只设置cookie
                # print(name, type(name))
                request.session['username'] = name
                request.session['is_login'] = True
                if request.POST.get('rmb', None) == '1':
                    print('选择了10天免登陆')
                    request.session.set_expiry(60*60*24*10)  # 10天免登陆访问
                if u_type == '1':
                    # res = redirect(reverse('user'))  # 这写法会导致cookie传值出错，原因未知,不要使用就行
                    return redirect('/usdb/user')
                    # 下面是只设置cookie
                    # res = redirect('/usdb/user/')
                    # res.set_cookie('usercookies', name, httponly=True)  # cookie的值不能是对象!
                elif u_type == '2':
                    # print('2222ogogogogogo')
                    return redirect('/usdb/manage/')
                    # 下面是只设置cookie
                    # res = redirect('/usdb/manage/')
                    # res.set_cookie('admincookies', name, httponly=True)
                # print("res:", res)
                # return res
                # return redirect('/usdb/manage/?' + "loginname" + "=" + name)
            else:
                if obj_name:
                    error_msg = "密码错误!"
                else:
                    error_msg = "用户不存在!"
                return render(request, 'login.html', {'error_msg': error_msg})


@csrf_protect
def registe(request):
    """
    注册
    :param request:
    :return:
    """
    if request.method == "GET":
        # group_list = [{'uid':1, 'caption':"前端组"}, {'uid':2, 'caption':"项目实施组"}] 测试用
        # print(models.InterestGroups.objects.all().values_list('id', 'name'))
        r_dic = {
            "username": '',
            "password": '',
            "password_2": '',
            "email": '',
            "phone": '',
            "u_type": 1,
            "w_group": 1,
            "i_group": []
        }
        rg_obj = registe_form.RFM(initial=r_dic)
        # print(rg_obj)
        return render(request, 'register.html', {'rg_obj': rg_obj})
    elif request.method == "POST":
        warninginfo = ""
        # print(request.POST)
        form = registe_form.RFM(request.POST)

        if form.is_valid():
            print("校验通过")
            try:
                test_err = int("测试异常情况下的日志记录功能使用,平时注释掉")
                if models.UserInfo.objects.filter(username=form.cleaned_data['username']) is None:
                    warninginfo = "用户已存在!"
                    return render(request, 'register.html', {'rg_obj': form, 'warning_info': warninginfo})  # 通过form返回错误信息
                else:
                    user_dic = {}
                    print(form.cleaned_data)
                    user_dic['username'] = form.cleaned_data['username']
                    user_dic['password'] = form.cleaned_data['password']
                    user_dic['phone'] = form.cleaned_data['phone']
                    user_dic['email'] = form.cleaned_data['email']
                    user_dic['user_group_id'] = form.cleaned_data['w_group']
                    user_dic['user_type_id'] = form.cleaned_data['u_type']

                    models.UserInfo.objects.create(**user_dic)  # 创建新用户了
                    user_obj_info = models.UserInfo.objects.get(username=form.cleaned_data['username'])
                    user_obj_info.interestgroups_set.add(*form.cleaned_data.get('i_group'))  # 多对多兴趣组关系绑定,必须小写!!
                    return HttpResponse("注册成功,请登陆!")
            except Exception as ex:
                warninginfo = "注册失败"
                # print(ex)
                handel_err_s.send(sender="db_err", err_type="db_write", content=ex)
                # 这里需要加一个类似SQL原生的事务回滚!!!!!!!!!!!!!!!!!!!!!!
                return render(request, 'register.html', {'rg_obj': form, 'warning_info': warninginfo})  # 通过form返回错误信息
        else:
            # print(form.errors.as_json())  # 打印出来的信息是unicode不方便分析
            print(form.errors)
            print("提交校验不通过")
            warninginfo = "注册失败"
            return render(request, 'register.html', {'rg_obj': form, 'warning_info': warninginfo})  # 通过form返回错误信息
        # name = request.POST.get('username', None)
        # email = request.POST.get('email', None)
        # phone = request.POST.get('phone', None)
        # password = request.POST.get('password', None)
        # u_type = request.POST.get('u_type', None)
        # group_id = request.POST.get('group_id', None)
        # obj_name = models.UserInfo.objects.filter(username=name).first()
        # print(name, email, phone, password, u_type, group_id)
        # if obj_name:
        #     warninginfo = "用户名已存在"
        #     return render(request, 'register.html', {'warning_info': warninginfo})
        # else:
        #     obj = models.UserInfo.objects.create(username=name, password=password, email=email,
        #                                             phone=phone, user_type_id=u_type, user_group=group_id)
        #     if obj:
        #         return HttpResponse("注册成功")
        #     else:
        #         return HttpResponse("注册失败")

# 只设置cookie方式
# @auth(0)
# def manage(request):
#     """
#     管理员
#     :param request:
#     :param username:
#     :return:
#     """
#     print("manage")
#     if request.method == "GET":
#         return render(request, 'admin.html')  # 进入到管理主界面


# session方式


@csrf_protect
def manage(request):
    """
    管理员
    :param request:
    :return:
    """
    if request.method == "GET":
        if request.session.get('is_login', None):
            return render(request, 'admin.html', {'admin_name': request.session['username']})
    return HttpResponse("非法访问,请先登陆!")


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

# 只设置cookie方式
# @auth(0)
# def getgroupinfo(request, type):
#     """
#     获取组信息
#     :param request:
#     :return:
#     """
#     print("获取用户组信息:")
#     g_list = models.WorkGroup.objects.all()
#     ig_list = models.InterestGroups.objects.all()
#     print(g_list)
#     if type == 1:
#         return render(request, 'admin.html', {'title_info': "用户组信息", 'hide': "cancelhide",
#                                                'group_list': g_list, 'igroup_list': ig_list, 'operation': "ok"})
#     elif type == 2:
#         return render(request, 'admin.html', {'title_info': "增加用户", 'group_list': g_list, 'igroup_list': ig_list, 'hide': "cancelhide_adusr"})


# session方式


@csrf_protect
def getgroupinfo(request, type):
    """
    获取组信息
    :param request:
    :return:
    """
    print("获取用户组信息:")
    if request.session.get('is_login', None):
        g_list = models.WorkGroup.objects.all()
        ig_list = models.InterestGroups.objects.all()
        print(g_list)
        if type == 1:
            return render(request, 'admin.html', {'title_info': "用户组信息", 'hide': "cancelhide",
                                                   'group_list': g_list, 'igroup_list': ig_list, 'operation': "ok"})
        elif type == 2:
            return render(request, 'admin.html', {'title_info': "增加用户", 'group_list': g_list, 'igroup_list': ig_list, 'hide': "cancelhide_adusr"})
    else:
        return HttpResponse("非法访问,请先登陆!")


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


U_LIST = []  # 存储人员

# 只设置cookie方式
# @auth(0)
# def getuserinfo(request):
#     """
#     用户信息
#     :param request:
#     :return:
#     """
#     from utils import pagination
#     print("获取用户信息")
#     print(request.GET)
#     current_page = request.GET.get('p', 1)  # 第几页
#     current_page = int(current_page)
#     print(request.COOKIES)
#
#     u_count = models.UserInfo.objects.count()
#     print("当前页:", current_page)
#     print("总共人员数:", u_count)
#     # per_page_count = 10
#     # pager_num = 7
#     # if u_count <= 7:
#     #     per_page_count = u_count
#     #     pager_num = 1
#     # elif u_count <= 70:
#     #     per_page_count = 1 + int(u_count/7)
#     # print(per_page_count, pager_num)
#     # page_obj = pagination.Page(current_page, u_count, per_page_count, pager_num)  # 默认一页十条,一共7页
#     page_obj = pagination.Page(current_page, u_count)  # 默认一页十条,一共7页
#
#     print(page_obj.start, page_obj.end)
#     u_list = models.UserInfo.objects.all()[page_obj.start: page_obj.end]  # 切片获取对应区间的
#     print(u_list)
#     page_str = page_obj.page_str("/usdb/getusers_info/")
#     return render(request, 'admin.html', {'title_info': "用户信息", 'hide': "canceluserhide",
#                                           'user_list': u_list, 'page_str': page_str})

# session方式


@csrf_protect
def getuserinfo(request):
    """
    用户信息
    :param request:
    :return:
    """
    if request.session.get('is_login', None):
        from utils import pagination
        print("获取用户信息")
        print(request.GET)
        current_page = request.GET.get('p', 1)  # 第几页
        current_page = int(current_page)
        print(request.COOKIES)

        u_count = models.UserInfo.objects.count()
        print("当前页:", current_page)
        print("总共人员数:", u_count)
        page_obj = pagination.Page(current_page, u_count)  # 默认一页十条,一共7页

        print(page_obj.start, page_obj.end)
        u_list = models.UserInfo.objects.all()[page_obj.start: page_obj.end]  # 切片获取对应区间的
        print(u_list)
        page_str = page_obj.page_str("/usdb/getusers_info/")
        return render(request, 'admin.html', {'title_info': "用户信息", 'hide': "canceluserhide",
                                              'user_list': u_list, 'page_str': page_str})
    else:
        return HttpResponse("非法访问,请先登陆!")


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
                m2mobj = models.UserInfo.objects.get(uid=uid).interestgroups_set.all()  # 反向查询,注意这个写法
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

# 只设置cookie方式
# @auth(0)
# def modifyuser_up(request, uid):
#     """
#     提交修改的用户资料
#     :param request:
#     :param uid:
#     :return:
#     """
#     print(uid)
#     print(request.POST)
#     result = 1
#     try:
#         models.UserInfo.objects.filter(id=uid).update(password=request.POST.get('pwd'),
#                                                       email=request.POST.get('email'),
#                                                       phone=request.POST.get('phone'),
#                                                       user_type_id=int(request.POST.get('m_choicelevel')),
#                                                       user_group=int(request.POST.get('m_choicegroup')))
#     except Exception as ex:
#         print(ex)
#         result = 0
#     return render(request, 'manage.html', {'operate_type': 7, 'operate_result': result})

# session方式


@csrf_protect
def modifyuser_up(request, uid):
    """
    提交修改的用户资料
    :param request:
    :param uid:
    :return:
    """
    if request.session.get('is_login', None):
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
    else:
        return HttpResponse("非法访问,请先登陆!")

# 只设置cookie方式
# @auth(1)
# def user(request):
#     """
#     普通用户
#     :param request:
#     :return:
#     """
#     print("user")
#     if request.method == "GET":
#         return render(request, 'user.html')  # 进入到用户主界面

# session方式


@csrf_protect
def user(request):
    """
    普通用户
    :param request:
    :return:
    """
    print("user")
    if request.method == "GET":
        if request.session.get('is_login', None):
            return render(request, 'user.html')  # 进入到用户主界面
    return HttpResponse("非法访问,请先登陆!")


def visitor(request):
    """
    游客
    :param request:
    :return:
    """
    pass
