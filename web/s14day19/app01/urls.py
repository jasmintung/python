from django.urls import path,include,re_path
from django.contrib import admin
from app01 import views

urlpatterns = [
    path('login/', views.login),
    path('index/', views.index),
    path('user_info/', views.user_info),
    re_path(r'^userdetail-(?P<nid>\d+)/', views.user_detail),  # path不支持url的正则,用re_path!!
    re_path(r'^userdel-(?P<nid>\d+)/', views.user_del),
    re_path(r'^useredit-(?P<nid>\d+)/', views.user_edit),
    path('orm/', views.orm),
]