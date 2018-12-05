from django.urls import path, re_path
from django.conf.urls import include
from .views import user

urlpatterns = [
    path('base-info.html', user.base_info),
    path('upload_file/', user.upload_file),
    re_path(r'^tag.html$', user.tag),
    re_path(r'^category.html$', user.category),
    re_path(r'^article.html$', user.article),
    re_path(r'^add-article.html$', user.add_article),
    re_path(r'^edit-article-(\d+).html$', user.edit_article),
]
