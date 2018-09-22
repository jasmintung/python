#!/usr/bin/env python
# -*- coding:utf-8 -*-
from io import BytesIO
import json
from django.shortcuts import HttpResponse, redirect
from django.shortcuts import render
from django.core import serializers
from utils.check_code import create_validate_code
from repository.models import UserInfo
from forms import login_form, registe_form
from django.core.exceptions import ValidationError


class JsonCustomEncoder(json.JSONEncoder):
    """
    解决出现两次序列化的问题
    """
    def default(self, field):
        if isinstance(field, ValidationError):
            return {'code': field.code, 'message': field.message}
        else:
            return json.JSONEncoder.default(self, field)


def auth(type):
    """
    装饰器做账户验证用
    :param type:
    :return:
    """
    def deco(func):
        def inner(request, *args, **kwargs):
            v = request.COOKIES.get('loginErrCount')
            if not v:
                return redirect('/login')
            else:
                # 这里记录尝试登录失败的次数
                print("try login failed count:", v)
            return func(request, *args, **kwargs)
        return inner
    return deco


def check_code(request):
    """
    验证码
    :param request:
    :return:
    """
    print("get check code...")
    stream = BytesIO()
    img, code = create_validate_code()
    img.save(stream, 'PNG')
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())


def login(request):
    """
    登陆
    :param request:
    :return:
    """

    if request.method == "GET":
        print("login..GET")
        # 特别注意,如果这里没有给LFGM初始化值,前端不会提示错误信息,原因尚没搞清楚!!!!
        dic = {
            'username': '',
            'password': '',
        }
        lg_obj = login_form.LGFM(dic)  # 必须给初始值
        print(lg_obj)
        return render(request, 'login.html', {'lg_obj': lg_obj})
    elif request.method == "POST":
        count = 0
        ret = {'statues': True, 'error': None, 'data': None}
        # print("login..POST")
        print(request.POST)
        print(request.POST.get('authcode'))
        cookie = request.COOKIES.get('errlgcnt', None)
        if cookie:
            print("cookie:", cookie)
            count = int(cookie)
            count += 1
        else:
            count = 1
        if request.session['CheckCode'].upper() == request.POST.get('authcode').upper() or (count < 3):
            lg_auth_form = login_form.LGFM(request.POST)
            if lg_auth_form.is_valid():
                print("通过")
                request.session['username'] = lg_auth_form.cleaned_data['username']
                print(request.session['username'])
                request.session['is_login'] = True
                ret['data'] = lg_auth_form.cleaned_data['username']
                # print(ret)
                return login_back(json.dumps(ret))
            else:
                print("校验不通过")
                # error_info = lg_auth_form.errors.as_json
                # print(error_info)
                print(
                    lg_auth_form.errors.as_data())  # 返回{'username': [ValidationError(['用户名不能为空'])], 'password': [ValidationError(['密码不能为空'])]}
                ret['statues'] = False
                ret['error'] = lg_auth_form.errors.as_data()
                # print(ret)
                result = json.dumps(ret, cls=JsonCustomEncoder)
                # print(result)
                # print(type(result))
                return login_back(result, count)
        else:
            ret['statues'] = False
            ret['data'] = "验证码错误"
            return login_back(json.dumps(ret), count)
            # return render(request, 'login.html', {'lg_obj': lg_auth_form})
        # print("session checkcode:", request.session['CheckCode'])
        # print("input checkcode:", request.POST.get('authcode'))
        # login_request_data = serializers.serialize("json", request.POST)
        # print(login_request_data)


def login_back(back, count=0):
    print(back)
    res = HttpResponse(back)
    res.set_cookie('errlgcnt', count, max_age=60 * 60)
    # cookie = request.COOKIES.get('errlgcnt', None)
    # cookie = request.get_signed_cookie('errlgcnt', None, salt='lgcookiecnt')  # 这样写,jsp暂时不知怎么解析
    # if cookie:
    #     print("cookie:", cookie)
    #     count = int(cookie)
    #     count += 1
    #     res.set_cookie('errlgcnt', count, max_age=60 * 60)
    #     # res.set_signed_cookie('errlgcnt', count, salt='lgcookiecnt', max_age=60*60)
    # else:
    #     res.set_cookie('errlgcnt', 1, max_age=60 * 60)
    #     # res.set_signed_cookie('errlgcnt', 0, salt='lgcookiecnt', max_age=60*60)
    return res


def register(request):
    """
    注册
    :param request:
    :return:
    """
    if request.method == "GET":
        print("GET:")
        print(request.GET)
        if request.GET.get('jump', None):
            print("next")
            # return HttpResponse('../backend/base-info.html')
            # return redirect('')
        else:
            dic = {
                'username': '',
                'password': '',
                'password2': '',
                'email': '',
            }
            rg_obj = registe_form.RGFM(dic)
            return render(request, 'register.html', {'rg_obj': rg_obj})
    elif request.method == "POST":
        print(request.POST)
        ret = {'statues': True, 'error': None, 'data': None}
        if request.session['CheckCode'].upper() == request.POST.get('authcode').upper():
            rg_auth_form = registe_form.RGFM(request.POST)
            if rg_auth_form.is_valid():
                print("data ok!")
                # rg_auth_form.clean()
                ret['error'] = "PASS"
                rg_data = rg_auth_form.get_registe_info()
                print(rg_data)
                ret['data'] = rg_data[0]
                # 这里写数据库
                UserInfo.objects.create(username=rg_data[0], password=rg_data[1], email=rg_data[2])
                # 加入session
                request.session['is_login'] = True
                # print(ret)
                return HttpResponse(json.dumps(ret))
            else:
                print(rg_auth_form.errors.as_data())  # 返回{'username': [ValidationError(['用户名不能为空'])], 'password': [ValidationError(['密码不能为空'])]}
                ret['error'] = rg_auth_form.errors.as_data()
                # print(ret)
                result = json.dumps(ret, cls=JsonCustomEncoder)
                print(result)
                print(type(result))
                return HttpResponse(result)
        else:
            ret['data'] = "验证码错误"
            return HttpResponse(json.dumps(ret))


def logout(request):
    """
    注销
    :param request:
    :return:
    """
    pass
