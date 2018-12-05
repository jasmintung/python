from django.shortcuts import render, redirect, HttpResponse

# Create your views here.


def login(request):
    from django.conf import settings
    # from django.core.handlers.wsgi import WSGIRequest
    print(settings)
    if request.method == "GET":
        # val = int("123123fdsfsdf")  # 测试process_exception执行情况
        # print("GET:")
        print(request.GET)
        print("--------------------------")
        # 注意!!!! X-CSRFtoken会被转换成:HTTP_X_CSRFTOKEN
        print(request.META.get('HTTP_X_CSRFTOKEN', None))  # 获取request headers头信息,根据key,针对前端ajax方式发送
        # print(request.environ)
        return render(request, 'login.html')
    elif request.method == "POST":
        print("POST:")
        print(request.POST)
        print(request.environ)
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        if user == 'root' and pwd == '123':
            request.session['username'] = user
            request.session['is_login'] = True
            print("session:", request.session)
            if request.POST.get('rmb', None) == '1':
                request.session.set_expiry(10)  # 10秒有效
            return redirect('/index/')
        else:
            return render(request, 'login.html')


from django.views.decorators.csrf import csrf_exempt, csrf_protect


@csrf_protect
def index(request):
    print(request.session.get('is_login', None))
    if request.session.get('is_login', None):
        return render(request, 'index.html', {'username': request.session['username']})
    else:
        return HttpResponse("gun")


def logout(request):
    """
    清除session
    :param request:
    :return:
    """
    # del request.session['username']  # 删除指定
    request.session.clear()  # 删除所有
    return redirect('/login/')


class Foo:
    def __init__(self, req, html, dic):
        self.req = req
        self.html = html
        self.dic = dic

    def render(self):
        # 创建钩子
        print("gouzi gogogo")
        return render(self.req, self.html, self.dic)


def test(request, nid):
    """
    测试process_template_response的执行情况
    :param request:
    :param nid:
    :return:
    """
    return Foo(request, 'index.html', {'k1': 'v1'})


from django.views.decorators.cache import cache_page


@cache_page(20)
def cache(request):  # 表示20秒刷新一次缓存
    """
    测试缓存
    :param request:
    :return:
    """
    import time
    ctime = time.time()
    return render(request, 'cache.html', {'ctime': ctime})


def signal(request):
    """
    Django信号测试,比如用在数据库操作之前记录一条日志
    :param request: 
    :return: 
    """
    from app01 import models

    print('1--models begin')
    obj = models.UserInf(user='root')
    print('end')
    # 这里会执行signals中的f1,因为f1是注册在pre_save信号中
    obj.save()

    print('2--models begin')
    obj = models.UserInf(user='root')
    print('end')
    # 这里会执行signals中的f1,因为f1是注册在pre_save信号中
    obj.save()

    print('3--models begin')
    obj = models.UserInf(user='root')
    print('end')
    # 这里会执行signals中的f1,因为f1是注册在pre_save信号中
    obj.save()

    from signals import pizza_done
    # 触发自定义信号,参数一样的情况下,不会系统不会反复执行,原因未知
    pizza_done.send(sender="asdfasdf", toppings=73373, size=456)

    return HttpResponse("OK")


################## Form ########################
from django import forms
from django.forms import widgets
from django.forms import fields


class FM(forms.Form):
    """
    下面这样创建后,就直接在本地浏览器html里创建了校验规则,直接本地校验,没有网络交互
    """
    user = fields.CharField(
        error_messages={'required': '用户名不能为空'},  # 校验规则
        widget=widgets.Textarea(attrs={'class': 'c1'}),  # 通过这个设置样式标签
        label="用户名",  # 这个相当于html里的空白标签,label
    )
    pwd = fields.CharField(
        max_length=12,
        min_length=6,
        error_messages={'required': '密码不能为空.', 'min_length': '密码长度不能小于6', 'max_length': "密码长度不能大于12"},
        widget=widgets.PasswordInput(attrs={'class': 'c2'})
    )
    email = fields.EmailField(error_messages={'required': '邮箱不能为空.', 'invalid': "邮箱格式错误"})

    f = fields.FileField()  # 选择文件

    city1 = fields.ChoiceField(
        choices=[(23, '北京'), (31, '天津'), (56, '上海'), (37, '广州')]
    )
    city2 = fields.MultipleChoiceField(
        choices=[(32, '成都'), (54, '深圳'), (77, '大连'), (89, '厦门')]
    )


from app01 import models


def fm(request):
    if request.method == "GET":
        # 模拟从数据库中把数据获取到然后直接整体传给模板
        dic = {
            "user": 'r1',
            "pwd": '123123',
            "email": 'fsadd',
            'city1': 1,
            'city2': [1, 3, 4]
        }
        obj = FM(initial=dic)
        return render(request, 'fm.html', {'obj': obj})
    elif request.method == "POST":
        # 获取用户所有数据
        # 每条熟请求的验证
        # 成功: 显示所有的正确信息
        # 失败: 现实错误的信息
        obj = FM(request.POST)
        r1 = obj.is_valid()
        if r1:
            models.UserInf.objects.create(**obj.cleaned_data)
        else:
            print("提交数据有问题")
            return render(request, 'fm.html', {'obj': obj})
        return render(request, 'fm.html')
