#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render, HttpResponse
from django.shortcuts import redirect
from repository import models


def index(request):
    """
    博客首页,展示全部博文,不用先登陆
    :param request:
    :return:
    """
    if request.method == "GET":
        print("main page")
        article_list = models.Article.objects.all()
        return render(request, 'index.html', {'article_list': article_list})


def home(request, site):
    """
    博主个人首页
    :param request:
    :param site: 博主的网站后缀如：http://xxx.com/zhangtong.html
    :return:
    """
    # if request.session.get('is_login', None): # 不需要验证,人人都可访问博客主页
    # print("enter home page")
    date_list = []
    print("site:", site)
    user_home = models.Blog.objects.filter(site=site).select_related('user').first()
    print("标题:", user_home.title)
    print("用户名:", user_home.user.username)
    print("昵称:", user_home.user.nickname)
    print("标签:", user_home.tag_set.all())
    tag_objs = user_home.tag_set.all()  # 反向查找
    cat_objs = user_home.category_set.all()  # 反向查找
    article_objs = user_home.article_set.all()  # 反向查找
    date_objs = user_home.article_set.filter(blog_id=user_home.nid).values("create_time")  # 这个查询屡试不爽.
    # print("atricle create time:", date_obj)
    for dates in date_objs:
        # print(dates.get('create_time', None))
        article_date = dates.get('create_time', None)
        # print(type(article_date))  # 类型datetime.datetime
        # print(article_date.year, article_date.month)  # 获取到年月日
        date_list.append(str(article_date.year) + '-' + str(article_date.month))
        # print(date_list)
    date_list = list(set(date_list))  # 去重
    print(date_list)
    # for item in tag_objs:
    #     print(item.title)
    if user_home:
        return render(request, 'home.html', {'user_home': user_home, 'tag_list': tag_objs, 'cat_list': cat_objs,
                                             'date_month_list': date_list, 'article_list': article_objs})
    else:
        return HttpResponse("访问的资源不存在!")
    # else:
    #     return HttpResponse("非法访问,请先登录!")


def filter(request, site, condition, val):
    """
    分类显示
    :param request:
    :param site:
    :param condition:
    :param val:
    :return:
    """
    user_home = models.Blog.objects.filter(site=site).select_related('user').first()
    if not user_home:
        return redirect('/')
    template_name = "home_summary_list.html"
    if condition == 'tag':
        template_name = "home_title_list.html"
        article_list = models.Article.objects.filter(tags__title=val, blog=user_home).all()
    elif condition == 'category':
        article_list = models.Article.objects.filter(category__title=val, blog=user_home).all()
    elif condition == 'date':
        article_list = models.Article.objects.filter(blog=user_home).extra(
            where=['date_format(create_time,"%%Y-%%m")=%s'], params=[val, ]).all()
    else:
        article_list = []

    return render(request, template_name)


def detail(request, site, nid):
    """
    博文详细页
    :param request:
    :param site:
    :param nid:
    :return:
    """
    return render(request, 'home_detail.html')

