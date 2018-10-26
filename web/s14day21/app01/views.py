from django.shortcuts import render, HttpResponse, redirect
import time
# Create your views here.
user_info = {
    'zhangtong': {'pwd': "1234"},
    'guankaiyu': {'pwd': "9876"},
}


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('pwd')
        dic = user_info.get(u)
        if not dic:
            print("用户不存在")
            return render(request, 'login.html')
        if dic['pwd'] == p:
            print("验证通过")
            res = redirect('/index/')
            res.set_cookie('zhangtong123!', u)  # 设置cookie,关闭浏览器后失效
            # res.set_cookie('zhangtong123!', u, max_age=10)  # 设置cookie,并设置5秒后失效
            # begin-----设置cookie,并设置截止时间失效时长为: 5秒
            # import datetime
            # current_time = datetime.datetime.utcnow()
            # current_time = current_time + datetime.timedelta(seconds=5)
            # res.set_cookie('zhangtong123!', u ,expires=current_time)
            # end-----设置cookie,并设置截止时间失效时长为: 5秒
            # 什么是HttpOnly? 如果您在cookie中设置了HttpOnly属性,那么通过js脚本将无法读取到cookie信息,这样能有效的防止XSS攻击
            res.set_cookie('user_type', "asdf", httponly=True)
            print("res:", res)
            return res
        else:
            print("验证不对.")
            return render(request, 'login.html')

# CBV


def auth(func):
    def inner(request, *args, **kwargs):
        v = request.COOKIES.get('zhangtong123!')
        print("local cookie:", v)
        time.sleep(5)  # 这个延时5秒主要是看cookie是在什么时候设置到浏览器的
        if not v:
            return redirect('/login/')
        return func(request, *args, **kwargs)
    return inner


@auth
def index(request):
    print("index")
    v = request.COOKIES.get("zhangtong123!")
    return render(request, 'index.html', {'current_user': v})


def tpl1(request):
    user_list = [1, 2, 3, 43]
    print("tpl1")
    return render(request, 'tpl1.html', {'u': user_list})


def tpl2(request):
    name = 'root'
    return render(request, 'tpl2.html', {'name': name})


def tpl3(request):
    status = "已经删除"
    return render(request, 'tpl3.html', {'status': status})


def tpl4(request):
    name = "IYMDFjfdf886sdf"
    return render(request, 'tpl4.html', {'name': name})


from utils import pagination
LIST = []
for i in range(500):
    LIST.append(i)


def user_list(request):
    isNull = True
    current_page = request.GET.get('p', 1)  # 第几页
    current_page = int(current_page)
    print(request.COOKIES)
    val = request.COOKIES.get('per_page_count',10)  # 每次显示多少条
    print("number:", val)
    val = int(val)
    # if isinstance(val, (str,)):
    #     isNull = False
    # else:
    #     isNull = True
    #     print("not ok")
    # print(val)
    # print(type(val))
    page_obj = pagination.Page(current_page, len(LIST), val)
    data = LIST[page_obj.start: page_obj.end]
    page_str = page_obj.page_str("/user_list/")
    # if not isNull:
    #     print("11111111")
    #     response = render(request, 'user_list.html', {'li': data, 'page_str': page_str})
    #     response.set_cookie('per_page_count', val)
    #     return response
    # else:
    #     print("22222222")
    #     # response = render(request, 'user_list.html', {'li': data, 'page_str': page_str})
    #     # response.set_cookie('per_page_count', val)
    #     # return response
    #     return render(request, 'user_list.html', {'li': data, 'page_str': page_str})
    return render(request, 'user_list.html', {'li': data, 'page_str': page_str})


from django import views
from django.utils.decorators import method_decorator


@method_decorator(auth, name="dispatch")
class Order(views.View):
    def get(self, request):
        v = request.COOKIES.get('zhangtong123!')
        return render(request, 'index.html', {'current_user': v})

    def post(self, request):
        v = request.COOKIES.get('zhangtong123!')
        return render(request, 'index.html', {'current_user': v})
