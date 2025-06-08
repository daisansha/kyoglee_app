from django.contrib import admin

# 経費申請モデルをインポート（現在使用中）
from accounting.models.expense_models import ExpenseApplication

# 徴収機能モデルも同一adminで管理（collection機能と共有）
from accounting.models.collection_models import Collection, CollectionRecord

# 経費申請を管理画面に登録
admin.site.register(ExpenseApplication)

# 徴収関連モデルも管理画面に登録
admin.site.register(Collection)
admin.site.register(CollectionRecord)
