from django.urls import path,include
from django.contrib import admin
from app02 import views

urlpatterns = [
    path('login/', views.login),
]
