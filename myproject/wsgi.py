"""
WSGI config for myproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/

Djangoの WSGI（同期）サーバー用のエントリポイント
Apache や gunicorn などでデプロイする時に使う
application = get_wsgi_application() が重要（サーバーがDjangoアプリを実行するための入り口）
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

application = get_wsgi_application()
