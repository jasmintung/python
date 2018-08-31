from django.urls import path, re_path
from usdb import views


urlpatterns = [
    path('login/', views.login),
    path('registe/', views.registe),
    path('add_group/', views.addgroup),
    path('manage/modifygroup/', views.getgroupinfo, {'type': 1}),
    path('manage/adduser/', views.getgroupinfo, {'type': 2}),
    # re_path(r'^getgroups_info-(?P<type>\d+)/', views.getgroupinfo),
    path('modify_group/', views.modifygroup),
    re_path(r'^modify_user_(?P<uid>\d+)/', views.modifyuser),
    path('add_users/', views.addusers),
    path('getusers_info/', views.getuserinfo),
    re_path(r'^getuddinfo-(?P<uid>\d+)/', views.userdetailinfo),
    re_path(r'^del_group-(?P<gid>\d+)/', views.delgroup),
    re_path(r'^del_user-(?P<uid>\d+)/', views.deluser),
    re_path(r'^user_up_modify_(?P<uid>\d+)/', views.modifyuser_up),
    # re_path(r'^manage_(?P<name>\w+)$', views.manage, name="manage"), # 此写法正则解析不出来,待分析??
    re_path(r'^manage/$', views.manage, name='manage'),
]
