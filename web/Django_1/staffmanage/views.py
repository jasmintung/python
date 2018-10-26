from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
import re
import json
# Create your views here.

from .models import session
from .models import UserInfo
from .models import StaffInfo


def login(request):
    error_msg = ""
    # 根据html中的name属性来解析
    print(request.method)
    if request.method == 'GET':
        print(session)
        return render(request, 'login.html', {'error_msg': error_msg})
    if request.method == 'POST':
        user = request.POST.get('user', None)
        pwd = request.POST.get('pwd', None)
        print(user, pwd)
        login_obj = session.query(UserInfo).filter(user == UserInfo.username, pwd == UserInfo.password).first()
        if login_obj:
            return redirect('/manage')
        else:
            error_msg = "用户名或密码错误"
    return render(request, 'login.html', {'error_msg': error_msg})


def manage(request):
    print(request.method)

    userlist = []
    operation = request.GET.get('operation', None)
    print("operation:", operation)
    # if operation is not None:
    # sql_select_all = "select *from staff_info"
    if request.method == 'GET':
        if operation is not None:
            if operation == "'viewall'":
                # print(session.execute(sql_select_all))
                user_datas = session.query(StaffInfo.id, StaffInfo.name, StaffInfo.age, StaffInfo.position, StaffInfo.phone).all()
                # user_data_dict = {} 写在这里的话会出现覆盖问题!详细解答请查看自己的云笔记
                for index in range(len(user_datas)):
                    user_data_dict = {}
                    user_data_dict["id"] = user_datas[index][0]
                    user_data_dict["username"] = user_datas[index][1]
                    user_data_dict["age"] = user_datas[index][2]
                    user_data_dict["position"] = user_datas[index][3]
                    user_data_dict["phone"] = user_datas[index][4]
                    # print(user_data_dict)
                    userlist.append(user_data_dict)
                    # print(userlist)
                return render(request, 'manage.html', {'hide': "surehide", 'user_list': userlist})
            # 下面部分代码还可以再简化下
            if operation.startswith("'delete'"):
                delete_str = operation.split('?')[1].strip()
                delete_id = int(delete_str.split('=')[1].strip())
                print(delete_id)
                try:
                    result = session.query(StaffInfo).filter_by(id=delete_id).first()
                    session.delete(result)
                    session.commit()
                    return HttpResponse("删除成功")
                except Exception as ex:
                    session.rollback()
                    return HttpResponse("删除失败" + ex)
            if operation.startswith("'detail'"):
                search_str = operation.split('?')[1].strip()
                search_id = int(search_str.split('=')[1].strip())
                print(search_id)
                return detail(request, search_id)
        else:
            return render(request, 'manage.html')
    if request.method == 'POST':
        if operation == "'addstaff'":
            # print(type(request.POST))  # <class 'django.http.request.QueryDict'>
            print(request.POST)
            # 后面学习发现这里可以用一个request.POST.getlist方法来获取多个值,lists获取具体值,元组形式返回
            str_querydict = str(request.POST)
            # print("start: %d endL %d" % (str_querydict.find('{'), str_querydict.find('}')))
            query_dict = str_querydict[str_querydict.find('{'): str_querydict.find('}')+1]
            ex_query_dict = json.loads(query_dict.replace("'", "\""))  # 必须要把单引号替换成双引号否则会报错
            # print(ex_query_dict.get('username')[0])  # 拿到姓名
            staff_numbers = len(ex_query_dict.get('username'))
            print("一共有%d名新增员工" % staff_numbers)
            # 写数据库
            if staff_numbers < 2:
                name = ex_query_dict.get('username')[0]
                age = int(ex_query_dict.get('age')[0])
                sex = ex_query_dict.get('sex')[0]
                phone = ex_query_dict.get('phone')[0]
                station = ex_query_dict.get('position')
                room_building = ex_query_dict.get('location')[0]
                origin = ex_query_dict.get('origin')[0]
                idnumber = ex_query_dict.get('idnumber')[0]
                obj = StaffInfo(name=name, id_number=idnumber, origin=origin, age=age,
                                sex=sex, phone=phone, address=room_building, position=station)
                session.add(obj)
            else:
                # 批量处理用下面的流程执行效率会高很多
                session.execute(StaffInfo.__table__.insert(), [{
                                                                'name': ex_query_dict.get('username')[i],
                                                                'age': int(ex_query_dict.get('age')[i]),
                                                                'sex': ex_query_dict.get('sex')[i],
                                                                'phone': ex_query_dict.get('phone')[i],
                                                                'origin': ex_query_dict.get('origin')[i],
                                                                'address': ex_query_dict.get('location')[i],
                                                                'position': ex_query_dict.get('position')[i],
                                                                'id_number': ex_query_dict.get('idnumber')[i]
                                                                } for i in range(staff_numbers)])
            try:
                session.commit()
            except Exception as ex:
                session.rollback()
                return HttpResponse("提交失败!")
            # 操作数据库
        return HttpResponse("提交成功!")


def detail(request, id):
    try:
        result = session.query(StaffInfo).filter_by(id=id).first()
        print(result.id_number)
        detail_info = {"username": result.name, "age": result.age, "sex": result.sex, "station": result.position,
                       "address": result.address, "idnumber": result.id_number, "phone": result.phone,
                       "origin": result.origin}
        print("fasfsadfsafsa:", detail_info)
        # redirect('/detail')
        return render(request, 'detail.html', {"detailinfo": detail_info})
        # return redirect('/detail', detailinfo=detail_info)
    except Exception as ex:
        return HttpResponse("请求数据失败!" + ex)




