from django.contrib import admin
from .models import Member, Role

# ===============================
# 管理画面で Role モデルをそのまま登録
# ===============================
admin.site.register(Role)

# ===============================
# Member モデルの管理画面カスタマイズ
# ===============================
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    # 以下のフィールドは読み取り専用（編集不可）にする
    readonly_fields = ["id", "created_at", "updated_at"]
    
    # 一覧表示で表示するカラムを指定
    list_display = ("name", "kyogleeid", "faculty", "part", "user")
    
    # サイドフィルタを表示（例：パートや期）
    list_filter = ("part", "kyogleeid")
    
    # デフォルトの並び順（kyogleeidの昇順）
    ordering = ["kyogleeid"]
    
    # 一覧表示画面で編集可能な項目
    list_editable=["user"]