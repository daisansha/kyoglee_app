# Django管理画面で Member モデルを操作可能にする
# id, created_at, updated_at は編集不可の読み取り専用に設定

from django.contrib import admin
from .models import Member
from .models import Role
#admin.site.register(Member)

admin.site.register(Role)

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "created_at", "updated_at"]