from django.apps import AppConfig

# ===============================
# Member アプリケーション設定
# ===============================
# この設定により、Djangoがこのアプリをプロジェクト内で認識できるようになる。
# settings.py の INSTALLED_APPS に 'member.apps.MemberConfig' を登録して使用。
class MemberConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # デフォルトの主キー型
    name = 'member'  # アプリのPythonパス（アプリフォルダ名と一致）
