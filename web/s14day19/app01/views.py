from django.shortcuts import render,HttpResponse,redirect
from app01 import models
# Create your views here.


def login(request):
    print(request.method)
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        u = request.POST.get('user')
        p = request.POST.get('pwd')
        # print(u, p)
        obj = models.UserInfo.objects.filter(username=u, password=p)
        # print(models.UserInfo.objects.all())
        # print(obj)
        if obj:
            return redirect('/cmdb/index/')
        else:
            return render(request, 'login.html')
    else:
        return redirect('/index/')


def index(request):
    return render(request, 'index.html')


def user_info(request):
    if request.method == "GET":
        print("用户信息:")
        user_list = models.UserInfo.objects.all()
        group_list = models.UserGroup.objects.all()
        print(group_list)
        return render(request, 'user_info.html', {'user_list': user_list, 'group_list': group_list})
    elif request.method == "POST":
        print("添加用户:")
        u = request.POST.get("user")
        p = request.POST.get("pwd")
        models.UserInfo.objects.create(username=u, password=p)
        return redirect('/cmdb/user_info')


def user_detail(request, nid):
    obj = models.UserInfo.objects.filter(id=nid).first()
    print("详细信息:", obj, nid)
    return render(request, 'user_detail.html', {'obj': obj})


def user_del(request, nid):
    print("删除用户:", nid)
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('cmdb/user_info/')


def user_edit(request, nid):
    if request.method == "GET":
        print("编辑用户:", nid)
        obj = models.UserInfo.objects.filter(id=nid).first()
        return render(request, 'user_edit.html', {'obj': obj})
    elif request.method == "POST":
        print("编辑用户提交")
        nid = request.POST.get('id')
        u = request.POST.get('username')
        p = request.POST.get('password')

        models.UserInfo.objects.filter(id=nid).update(username=u, password=p)
        return redirect('/cmdb/user_info/')


def orm(request):
    return HttpResponse('orm')
