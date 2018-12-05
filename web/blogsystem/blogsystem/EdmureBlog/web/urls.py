"""EdmureBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import re_path, path
from django.conf.urls import include
from .views import home
from .views import account

urlpatterns = [
    path('login/', account.login),
    path('register/', account.register),
    path('check_code.html/', account.check_code),
    re_path(r'^(?P<site>\w+).html', home.home),
    re_path(r'^(?P<site>\w+)/(?P<condition>((tag)|(date)|(category)))/(?P<val>\w+-*\w+).html', home.filter),
    re_path(r'^(?P<site>\w+)/(?P<nid>\d+).html', home.detail),
    path('', home.index),
]
