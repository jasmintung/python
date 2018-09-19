#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import os
from django.shortcuts import render, HttpResponse, redirect
from repository.models import UserInfo, Blog, Tag, Category
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def base_info(request):
    """
    博主个人信息,session验证
    :param request:
    :return:
    """
    if request.session.get('is_login', None):
        if request.method == "GET":
            print(request.GET)
            username = ""
            user_obj = ""
            blog_obj = ""
            info = request.GET.lists()  # 返回列表形式的元祖(key, value)集合
            for index in info:
                username = index[0]  # 获得key,这里也就是获得GET方式请求的用户名
            obj = UserInfo.objects.filter(username=username).values()
            b_obj = Blog.objects.filter(user__username=username).values()
            print(b_obj)
            for index in obj:
                user_obj = index  # 用户信息---字典
            # print(user_obj)
            for index in b_obj:
                blog_obj = index  # 博客信息---字典
            return render(request, 'backend_base_info.html', {'usr_obj': user_obj, 'blog_obj': blog_obj})
        elif request.method == "POST":
            ret = {'statues': True, 'error': "保存成功!", 'data': None}
            print(request.POST)
            update_info = ""
            for key in request.POST.lists():
                update_info = json.loads(key[0])  # 解析ajax穿过来的数据
            username = update_info.get("username", None)
            title = update_info.get("blogtitle", None)
            nickname = update_info.get("nickname", None)
            site = update_info.get("blogurl", None)
            print("site_url:", site)
            theme = update_info.get("blogtheme", None)
            usr_obj = UserInfo.objects.filter(username=username).first()
            if usr_obj:
                if UserInfo.objects.filter(blog__user=usr_obj).first():
                    # print("已开通博客的情况下修改!")
                    # UserInfo.objects.filter(username=username).update(nickname=nickname)
                    nid_dic = UserInfo.objects.filter(username=username).values("nid")
                    for item in nid_dic:
                        # print("nid:", item.get('nid'))
                        Blog.objects.filter(user_id=item.get('nid')).update(title=title, theme=theme, site=site)
                else:
                    blog_obj = Blog.objects.create(title=title, site=site, theme=theme, user=usr_obj)
                    blog_obj.save()
            return HttpResponse(json.dumps(ret))
    else:
        return HttpResponse("非法访问,请先登录!")
# @csrf_protect
# def base_info(request):
#     """
#     博主个人信息,有session
#     :param request:
#     :return:
#     """
#     print(request.GET)
#     if request.method == "GET":
#         if request.session.get('is_login', None):
#             username = ""
#             info = request.GET.lists()  # 返回列表形式的元祖(key, value)集合
#             for index in info:
#                 username = index[0]  # 获得key,这里也就是获得GET方式请求的用户名
#             obj = UserInfo.objects.filter(username=username).values()
#             print(obj)
#             return render(request, 'backend_base_info.html', {'usr_obj': obj})
#         else:
#             return HttpResponse("非法访问,请先登录!")


def tag(request):
    """
    博主个人标签管理
    :param request:
    :return:
    """
    ret = {'statues': True, 'error': "标签名已存在!", 'data': None}
    if request.method == "GET":
        tag_list = []
        obj = Tag.objects.all().values()
        print(obj)
        for index in obj:
            tag_list.append(index)
        print(tag_list)
        return render(request, 'backend_tag.html', {'tag_list': tag_list})
    elif request.method == "POST":
        tag_info = ""
        for key in request.POST.lists():
            tag_info = json.loads(key[0])  # 解析ajax穿过来的数据
        tag_name = tag_info.get('tagname', None)
        print(tag_name)
        if Tag.objects.filter(title=tag_name).first():
            print("已存在")
            return HttpResponse(json.dumps(ret))
        else:
            obj = Tag.objects.create(title=tag_name, blog_id=1)
            obj.save()
            # return render(request, 'backend_tag.html')
            return redirect('/backend/tag.html')


def category(request):
    """
    博主个人分类管理
    :param request:
    :return:
    """
    ret = {'statues': True, 'error': "分类名已存在!", 'data': None}
    if request.method == "GET":
        ct_list = []
        obj = Category.objects.all().values()
        print(obj)
        for index in obj:
            ct_list.append(index)
        print(ct_list)
        return render(request, 'backend_category.html', {'cat_list': ct_list})
    elif request.method == "POST":
        cat_info = ""
        for key in request.POST.lists():
            cat_info = json.loads(key[0])  # 解析ajax穿过来的数据
        cat_name = cat_info.get('catname', None)
        print(cat_name)
        if Category.objects.filter(title=cat_name).first():
            print("已存在")
            return HttpResponse(json.dumps(ret))
        else:
            obj = Category.objects.create(title=cat_name, blog_id=1)
            obj.save()
            # return render(request, 'backend_tag.html')
            return redirect('/backend/category.html')


def article(request):
    """
    博主个人文章管理
    :param request:
    :return:
    """
    return render(request, 'backend_article.html')


def add_article(request):
    """
    添加文章
    :param request:
    :return:
    """
    return render(request, 'backend_add_article.html')


def edit_article(request):
    """
    编辑文章
    :param request:
    :return:
    """
    return render(request, 'backend_edit_article.html')


def upload_file(request):
    """
    头像上传
    :param request:
    :return:
    """
    saveimgname = request.POST.get("username")
    print("save img name:", saveimgname)
    file_obj = request.FILES.get("fileupload")
    # 完全存服务器
    print("source file name:", file_obj.name)
    suffix = file_obj.name.split('.')[1]  # 获取后缀,在前端最好做一个图片格式简单校验
    print(suffix)
    img_path = os.path.join('static/imgs/', saveimgname + '.' + suffix)
    with open(img_path, 'wb') as f:
        for data in file_obj.chunks():
            f.write(data)
    ret = {'code': True, 'data': img_path}
    print(ret)
    # 使用Django ImageField,目前的情况图片没有存到指定目录,待研究
    file_obj.name = saveimgname + '.' + suffix
    UserInfo.objects.filter(username=request.POST.get("username")).update(avatar=file_obj)
    return HttpResponse(json.dumps(ret))
