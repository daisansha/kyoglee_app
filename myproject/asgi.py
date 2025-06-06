"""
ASGI config for myproject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/

Djangoの ASGIサーバー用のエントリポイント
非同期対応（WebSocketなど）をする場合に使う
application = get_asgi_application() により、ASGIサーバーからアプリケーションを起動できるようにする
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

application = get_asgi_application()
