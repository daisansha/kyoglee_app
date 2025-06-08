import os
from django.core.wsgi import get_wsgi_application

# ==============================
# WSGI（Web Server Gateway Interface）の設定ファイル
# ==============================
# このファイルは、DjangoアプリをApacheやgunicornなどのWSGIサーバーで動かすための
# エントリーポイントとして使用される。特に本番環境で利用される。

# 使用するDjango設定ファイルを指定
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# WSGIアプリケーションを取得（サーバーがこれを通じてDjangoアプリを起動）
application = get_wsgi_application()