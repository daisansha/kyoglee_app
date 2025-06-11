from django.db import models
from member.models import Member  # 団員モデルとのリレーションに使用
from django.utils import timezone
from cloudinary.models import CloudinaryField  # レシート画像保存用

# =======================================
# 経費申請情報を管理するモデル
# =======================================
class ExpenseApplication(models.Model):
    # 申請の承認状況（申請中・承認・却下）
    APPROVAL_CHOICES = [
        ('pending', '申請中'),
        ('refunded', '承認'),
        ('rejected', '却下'),
    ]

    # 払い戻し状況（未払い・払い済み）
    PAYMENT_CHOICES = [
        ('unpaid', '未払い'),
        ('paid', '払い済み'),
    ]

    # 申請者（団員）
    applicant = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name='expenses',  # Memberから辿るときに使う名前
        verbose_name="申請者"
    )

    # 申請項目
    title = models.CharField(
        max_length=50,
        verbose_name="項目",
        default="無題"
    )

    # 経費の内容（用途）
    description = models.CharField(
        max_length=255,
        verbose_name="用途・説明"
    )

    # 金額（整数、円単位）
    amount = models.IntegerField(
        verbose_name="金額（円）"
    )

    # 領収書画像（Cloudinaryに保存、任意）
    receipt_image = CloudinaryField(
        '画像',
        blank=True,
        null=True
    )

    # 申請日（デフォルトは現在日時）
    submitted_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="申請日時"
    )

    # 承認ステータス（初期値：申請中）
    approval_status = models.CharField(
        max_length=10,
        choices=APPROVAL_CHOICES,
        default='pending',
        verbose_name="承認ステータス"
    )

    # 支払ステータス（初期値：未払い）
    payment_status = models.CharField(
        max_length=10,
        choices=PAYMENT_CHOICES,
        default='unpaid',
        verbose_name="支払ステータス"
    )

    def __str__(self):
        return f"{self.applicant} - {self.amount}円 - {self.approval_status} / {self.payment_status}"