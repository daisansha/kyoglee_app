# ログイン機能
# accounts アプリで使用するURLパターンを定義。
# Djangoが提供する標準のログイン／ログアウトビューをそのまま利用。
# templates/registration/login.html がログイン画面のテンプレートとして使用される（カスタマイズ可能）
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

app_name = "accounts"
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]