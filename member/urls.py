from django.urls import path
from . import views

# アプリケーション名を指定（テンプレート内で名前空間付きでURLを参照できる）
# 例：{% url 'member:member_list' %}
app_name = "member"

# ===============================
# MemberアプリのURLパターン一覧
# ===============================
# 各URLがどのビュー関数に対応するかを定義

urlpatterns = [
    path("", views.index, name="index"),  # 初期ページ（トップ、ダッシュボードなど）

    path("create/", views.member_create, name="member_create"),  # 団員の新規登録フォーム

    path("list/", views.member_list, name="member_list"),  # 団員一覧ページ

    path("<uuid:id>/", views.member_detail, name="member_detail"),  # 個別団員の詳細ページ（UUIDで指定）

    path("<uuid:id>/update/", views.member_update, name="member_update"),  # 団員情報の編集ページ

    path("<uuid:id>/delete/", views.delete_member, name="member_delete"),  # 団員の削除処理（確認付き）
]