#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import os
from django.shortcuts import render, HttpResponse, redirect
from repository.models import UserInfo, Blog, Tag, Category, Article, Article2Tag, ArticleDetail
from django.views.decorators.csrf import csrf_protect
from forms import add_article_form


@csrf_protect
def base_info(request):
    """
    博主个人信息,session验证
    :param request:
    :return:
    """
    # 以下这样方式获取IP的原因是:
    # 但是有些网站服务器会使用ngix等代理http，或者是该网站做了负载均衡，导致使用remote_addr抓取到的是1270.0.1，
    # 这时使用HTTP_X_FORWARDED_FOR才获得是用户的真实IP
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    print("IP:", ip)  # 获取IP的目的是用于前端博客地址显示拼接,存数据库的是博客地址前缀
    if request.session.get('is_login', None):
        if request.method == "GET":
            print(request.GET)
            # username = ""
            username = request.session.get('username', None)  # 用session方式保存username
            user_obj = ""
            blog_obj = ""
            # info = request.GET.lists()  # 返回列表形式的元祖(key, value)集合
            # for index in info:
            #     username = index[0]  # 获得key,这里也就是获得GET方式请求的用户名
            # if len(username) == 0:
            #     username = request.session.get('username', None)
            # else:
            #     if username != request.session.get('username', None):
            #         pass
            obj = UserInfo.objects.filter(username=username).values()
            b_obj = Blog.objects.filter(user__username=username).values()
            print(b_obj)
            for index in obj:
                user_obj = index  # 用户信息---字典
            # print(user_obj)
            for index in b_obj:
                blog_obj = index  # 博客信息---字典
            return render(request, 'backend_base_info.html', {'usr_obj': user_obj, 'blog_obj': blog_obj, 'IP': ip})
        elif request.method == "POST":
            ret = {'statues': True, 'error': "保存成功!", 'data': None}
            print(request.POST)
            update_info = ""
            for key in request.POST.lists():
                update_info = json.loads(key[0])  # 解析ajax穿过来的数据
            username = update_info.get("username", None)
            if request.session.get('username', None) != username:  # 防止前端暴力修改提交信息
                return HttpResponse("非法访问,请先登录!")
            title = update_info.get("blogtitle", None)
            nickname = update_info.get("nickname", None)
            site = update_info.get("blogurl", None)
            # print("site_url:", site)
            start_index = site.rfind("/")
            end_index = site.rfind(".html")
            # print(start_index, end_index)
            site = site[start_index+1:end_index]
            # print("site", site)
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


def tag(request, inner_call=False):
    """
    博主个人标签管理
    :param request:
    :return:
    """
    ret = {'statues': True, 'error': "添加成功!", 'data': None}
    username = request.session.get('username', None)
    if username:
        if request.method == "GET":
            tag_list = []

            nid_dic = UserInfo.objects.filter(username=username).values("nid")
            for item in nid_dic:
                # print("nid:", item.get('nid'))
                bid_dic = Blog.objects.filter(user_id=item.get('nid')).values('nid')
                for ids in bid_dic:
                    obj = Tag.objects.filter(blog_id=ids.get('nid', None)).values()
                    print(obj)
                    for index in obj:
                        tag_list.append(index)
                    print(tag_list)
            if inner_call:
                return tag_list
            else:
                return render(request, 'backend_tag.html', {'tag_list': tag_list})
        elif request.method == "POST":
            tag_list = []
            tag_info = ""
            blog_id = 0
            # has_tag = False
            for key in request.POST.lists():
                tag_info = json.loads(key[0])  # 解析ajax穿过来的数据
            tag_name = tag_info.get('tagname', None)
            print(tag_name)
            username = request.session.get('username', None)
            if username:
                obj = Tag.objects.select_related('blog__user')
                # print(obj)
                for item in obj:
                    print(item.blog.user.username)
                    if username == item.blog.user.username:
                        tag_list.append(item.title)

                print(tag_list)
                if tag_name in tag_list:
                    print("已存在")
                    ret['statues'] = False
                    ret['error'] = "标签重复!"
                    return HttpResponse(json.dumps(ret))
                else:
                    nid_dic = Blog.objects.filter(user__username=username).values('nid')  # 获取对应Blog的ID
                    # print('blog ids:', nid_dic)
                    for bids in nid_dic:
                        blog_id = bids.get('nid', None)
                        print(blog_id)
                    obj = Tag.objects.create(title=tag_name, blog_id=blog_id)
                    obj.save()
                    return HttpResponse(json.dumps(ret))
            else:
                return redirect('/backend/tag.html')


def category(request, inner_call=False):
    """
    博主个人分类管理
    :param request:
    :return:
    """
    ret = {'statues': True, 'error': "添加成功!", 'data': None}
    username = request.session.get('username', None)
    if username:
        if request.method == "GET":
            cat_list = []

            nid_dic = UserInfo.objects.filter(username=username).values("nid")
            for item in nid_dic:
                # print("nid:", item.get('nid'))
                bid_dic = Blog.objects.filter(user_id=item.get('nid')).values('nid')
                for ids in bid_dic:
                    obj = Category.objects.filter(blog_id=ids.get('nid', None)).values()
                    print(obj)
                    for index in obj:
                        cat_list.append(index)
                    print(cat_list)
            if inner_call:
                return cat_list
            else:
                return render(request, 'backend_category.html', {'cat_list': cat_list})
        elif request.method == "POST":
            cat_list = []
            cat_info = ""
            blog_id = 0
            for key in request.POST.lists():
                cat_info = json.loads(key[0])  # 解析ajax穿过来的数据
            cat_name = cat_info.get('catname', None)
            print(cat_name)
            username = request.session.get('username', None)
            if username:
                obj = Category.objects.select_related('blog__user')
                # print(obj)
                for item in obj:
                    print(item.blog.user.username)
                    if username == item.blog.user.username:
                        cat_list.append(item.title)
                print(cat_list)
                if cat_name in cat_list:
                    print("已存在")
                    ret['statues'] = False
                    ret['error'] = "分类重复!"
                    return HttpResponse(json.dumps(ret))
                else:
                    nid_dic = Blog.objects.filter(user__username=username).values('nid')  # 获取对应Blog的ID
                    # print('blog ids:', nid_dic)
                    for bids in nid_dic:
                        blog_id = bids.get('nid', None)
                        print(blog_id)
                    obj = Category.objects.create(title=cat_name, blog_id=blog_id)
                    obj.save()
                    return HttpResponse(json.dumps(ret))
            else:
                return redirect('/backend/category.html')


def article(request):
    """
    博主个人文章管理
    :param request:
    :return:
    """
    blog_id = 0
    article_obj = ""
    username = request.session.get('username', None)
    if username:
        usr_obj = UserInfo.objects.filter(username=username).first()
        blog_ids = Blog.objects.filter(user=usr_obj).values("nid")
        for nid in blog_ids:
            blog_id = nid.get("nid", None)
        article_obj = Article.objects.filter(blog_id=blog_id)
    return render(request, 'backend_article.html', {'atc_obj': article_obj})


@csrf_protect
def add_article(request):
    """
    添加文章
    :param request:
    :return:
    """
    username = request.session.get('username', None)
    if username:
        usr_obj = UserInfo.objects.filter(username=username).first()
        print("blog nid:", usr_obj.blog.nid)  # onetoonefield正向查询,得到blog的nid
        blog_id = usr_obj.blog.nid
        if request.method == "GET":
            # dic = {
            #     'title': '',
            #     'summary': '',
            #     'read_count': 0,
            #     'comment_count': 0,
            #     'up_count': 0,
            #     'down_count': 0,
            #     'blog': blog_id
            # }
            # article_obj = add_article_form.ArticleModelForm(initial=dic)
            article_obj = add_article_form.ArticleModelForm(initial={'blog_id': usr_obj.blog.nid})
            article_detaile_obj = add_article_form.ArticleDetailModelForm()
            tag_list = tag(request, True)
            cat_list = category(request, True)
            print(article_obj)
            return render(request, 'backend_add_article.html', {'atc_obj': article_obj, 'atc_dtl_obj': article_detaile_obj,
                                                                'tag_obj': tag_list, 'cat_obj': cat_list, 'blog_id': blog_id})
        elif request.method == "POST":
            print(request.POST)

            atc_obj = add_article_form.ArticleModelForm(request.POST)
            if atc_obj.is_valid():
                # obj = atc_obj.save(False)
                # obj.blog_id = usr_obj.blog.nid
                # print(obj.tags)
                # # obj.article_type = '4'
                # obj.save()
                # atc_obj.save_m2m()
                # for item in request.POST:
                #     print(item)
                cat_obj = Category.objects.filter(nid=request.POST.get('category', None)).first()
                print("类型对象:", cat_obj)
                article_obj = Article.objects.create(title=request.POST.get('title'), summary=request.POST.get('summary'),
                                                     read_count=0, comment_count=0, up_count=0, down_count=0,
                                                     blog=usr_obj.blog, category=cat_obj,
                                                     article_type=request.POST.get('article_type'))
                print("文章对象:", article_obj)
                tags = request.POST.getlist('tags', None)
                # print(tags)
                for item in tags:
                    tag_obj = Tag.objects.filter(nid=item).first()
                    print(tag_obj)
                    Article2Tag.objects.create(article=article_obj, tag=tag_obj)
                atc_dt_obj = add_article_form.ArticleDetailModelForm(request.POST)
                print("---------------------------------------")
                if atc_dt_obj.is_valid():
                    print(request.POST.get('content', None))
                    ArticleDetail.objects.create(content=request.POST.get('content', None), article=article_obj)
                else:
                    print("222not pass")
                    print(atc_dt_obj.errors)
            else:
                print("111not pass")
                print(atc_obj.errors)


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
