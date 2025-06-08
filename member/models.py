from django.db import models
from django.contrib.auth.models import User
import uuid
from cloudinary.models import CloudinaryField

# =========================
# 団員の役職を定義するモデル
# =========================
class Role(models.Model):
    code = models.CharField(max_length=50)  # プログラム内で識別するためのコード（例：Zaimu）
    label = models.CharField(max_length=100)  # ユーザー向け表示用ラベル（例：財務）

    def __str__(self):
        return self.label

# =========================
# 団員情報を保存するモデル
# =========================
class Member(models.Model):
    # パートの選択肢（男声四部）
    PART_CHOICES = [
        ('top', 'トップ'),
        ('second', 'セカンド'),
        ('baritone', 'バリトン'),
        ('bass', 'ベース'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID"
    )  # 主キーとしてUUIDを使用（安全性・衝突回避）

    name = models.CharField(max_length=100, verbose_name="名前")  # 団員名
    
    kyogleeid = models.IntegerField(verbose_name="期")  # 何期生か（整数）
    
    joinyear = models.IntegerField(verbose_name="入団年")  # 入団年度
    
    faculty = models.CharField(max_length=100, verbose_name="所属")  # 学部など

    part = models.CharField(
        max_length=10,
        choices=PART_CHOICES,
        verbose_name="パート"
    )  # 所属パート（選択式）

    role = models.ManyToManyField(
        Role,
        verbose_name="役職",
        blank=True
    )  # 複数の役職と多対多で紐づけ

    picture = CloudinaryField(
        '画像',
        blank=True,
        null=True
    )  # Cloudinaryに保存されるプロフィール画像

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="作成日時"
    )  # 登録された日時（自動記録）

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="更新日時"
    )  # 最終更新日時（自動記録）

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )  # Djangoのログインユーザーと紐づけ（任意）

    def __str__(self):
        return self.name  # 管理画面や表示時に名前が表示される

    @property
    def is_financial(self):
        """役職に財務（code='Zaimu'）が含まれているか判定"""
        return self.role.filter(code='Zaimu').exists()