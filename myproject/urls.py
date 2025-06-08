from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

# ================================
# プロジェクト全体のURLルーティング設定
# ================================
# 各アプリのURL設定を include() でまとめて取り込む

urlpatterns = [
    path('admin/', admin.site.urls),  # 管理画面（/admin/）

    # 認証関連（ログイン・ログアウト）
    path('accounts/', include('accounts.urls')),  # 独自accountsアプリのURL設定
    path('', include('django.contrib.auth.urls')),  # Django組み込みの認証ビュー（login/logout/password等）

    # メイン画面（トップページとして利用）
    path('main/', include('main.urls')),

    # 団員情報管理（memberアプリ）
    path('member/', include('member.urls')),

    # 会計機能（徴収、経費）
    path('accounting/', include('accounting.urls', namespace='accounting')),

    # 練習管理（出欠や練習予定）
    path('practice/', include('practice_management.urls', namespace='practice_management')),

    # トップページ（/）にアクセスがあった場合は /main/ にリダイレクト
    path('', lambda request: redirect('/main/')),
]

# ================================
# メディアファイルの配信（開発環境のみ）
# ================================
# DEBUG=True のときだけ、mediaファイルへのURLアクセスを許可
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)