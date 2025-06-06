# URLとビュー関数の対応表
# uuid を使ってメンバー個別ページにアクセス
# app_name によりテンプレート内で {% url 'member:member_list' %} のように呼び出せる

from django.urls import path
from . import views

app_name = "member"
# このアプリにアクセスが来たとき、どの関数（ビュー）で処理するかを定義
#path("パス（トップページは空）",そのパスに対して動かす関数,name="このプロジェクトにおける名前")
urlpatterns = [
    path("", views.index, name="index"), 
    path("create/", views.member_create, name="member_create"),
    path("list/", views.member_list, name="member_list"),
    path("<uuid:id>/", views.member_detail, name="member_detail"),
    path("<uuid:id>/update/", views.member_update, name="member_update"),
    path("<uuid:id>/delete/", views.delete_member, name="member_delete"),
]