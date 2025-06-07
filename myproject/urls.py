"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect  # ← 追加

#プロジェクト全体のルーティング　アプリケーションごとにルーティング　アプリが増えたらここにpath("newapp/", include("newapp.urls")) を追加する
# include() で、各アプリ（management, accounts）の URL 設定を取り込んでいる
urlpatterns = [
    path('admin/', admin.site.urls), #管理画面
    path('accounts/', include('accounts.urls')),#ログイン・ログアウト用 accountsフォルダのurls.pyとひもづけ
    path('main/', include('main.urls')),
    path("member/", include("member.urls")), #パスmember/ と　ファイルmember.urls.pyをひもづけ
    path('', include('django.contrib.auth.urls')),
    path("accounting/", include("accounting.urls", namespace="accounting")),
    path("practice/", include("practice_management.urls", namespace="practice_management")),
    path('', lambda request: redirect('/main/')),  # ← トップページを /main/ に転送
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 開発環境（DEBUG=True）のときだけ、media/ にアクセスできるURLパターンを追加する」
#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)