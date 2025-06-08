from django.db import models
from member.models import Member  # 団員モデルを参照

# ==========================================
# 徴収項目（例：団費、演奏会費など）を管理するモデル
# ==========================================
class Collection(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="徴収項目"
    )  # 徴収の名前（例：2025年5月団費）

    content = models.TextField(
        verbose_name="徴収内容",
        blank=True
    )  # 補足内容（空欄可）

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="作成日"
    )  # 作成日時（自動記録）

    deadline = models.DateField(
        verbose_name="徴収期限日"
    )  # 支払いの締切日

    def __str__(self):
        return f"{self.title}（{self.deadline}）"

# ==========================================
# 個別の団員に対する徴収記録（実際の金額・ステータスなど）を管理
# ==========================================
class CollectionRecord(models.Model):
    STATUS_CHOICES = [
        ('未', '未'),       # 未払い
        ('済', '済'),       # 支払済み
        ('不要', '不要'),   # 不要（免除など）
    ]

    collection = models.ForeignKey(
        Collection,
        on_delete=models.CASCADE,
        related_name='records'
    )  # 対象となる徴収項目

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE
    )  # 対象団員

    amount = models.PositiveIntegerField(
        verbose_name="徴収額",
        default=0
    )  # 金額（円）

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='未',
        verbose_name="徴収ステータス"
    )  # 支払い状況の区分

    def __str__(self):
        return f"{self.member.name} - {self.amount}円 - {self.status}"