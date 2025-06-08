import os
from django.core.asgi import get_asgi_application

# ==============================
# ASGI（Asynchronous Server Gateway Interface）の設定ファイル
# ==============================
# Djangoアプリを非同期サーバー（例：Daphne, Uvicorn）で動かすときのエントリーポイント。
# WebSocket、HTTP2などの非同期通信に対応するために使う。

# 使用するDjangoの設定ファイルを指定
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# ASGIアプリケーションを取得（非同期サーバーがこれを通じてDjangoアプリを起動）
application = get_asgi_application()