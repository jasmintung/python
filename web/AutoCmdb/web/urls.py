from django.urls import path, re_path
from django.conf.urls import include
from django.contrib import admin
from web.views import account
from web.views import home
from web.views import asset
from web.views import user

urlpatterns = [
    re_path(r'^login.html$', account.LoginView.as_view()),
    re_path(r'^logout.html$', account.LogoutView.as_view()),
    re_path(r'^index.html$', home.IndexView.as_view()),
    re_path(r'^cmdb.html$', home.CmdbView.as_view()),

    re_path(r'^asset.html$', asset.AssetListView.as_view()),
    re_path(r'^assets.html$', asset.AssetJsonView.as_view()),

    re_path(r'^idc.html$', asset.IDCListView.as_view()),
    re_path(r'^idcjson.html$', asset.IDCJsonView.as_view()),

    re_path(r'^asset-(?P<device_type_id>\d+)-(?P<asset_nid>\d+).html$', asset.AssetDetailView.as_view()),
    re_path(r'^add-asset.html$', asset.AddAssetView.as_view()),

    re_path(r'^users.html$', user.UserListView.as_view()),
    re_path(r'^user.html$', user.UserJsonView.as_view()),

    re_path(r'^chart-(?P<chart_type>\w+).html$', home.ChartView.as_view()),
]
