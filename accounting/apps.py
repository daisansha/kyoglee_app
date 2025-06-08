from django.apps import AppConfig

# accounting アプリの設定
class AccountingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # IDフィールドのデフォルト設定
    name = 'accounting'  # アプリ名（プロジェクト内でのパス）