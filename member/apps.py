# Djangoにこのアプリ（member）を認識させるための基本設定
# INSTALLED_APPS に登録されている必要あり

from django.apps import AppConfig


class MemberConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'member'
