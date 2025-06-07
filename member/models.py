# 団員情報を保存するためのデータベースモデル
# __str__ によって、管理画面や一覧で名前が表示される

from django.db import models
from django.contrib.auth.models import User
import uuid
from cloudinary.models import CloudinaryField

class Role(models.Model):
    code = models.CharField(max_length=50)
    label = models.CharField(max_length=100)

    def __str__(self):
        return self.label

class Member(models.Model):
    PART_CHOICES = [
        ('top', 'トップ'),
        ('second', 'セカンド'),
        ('baritone', 'バリトン'),
        ('bass', 'ベース'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")#主キー　自動生成　編集不可
    name = models.CharField(max_length=100, verbose_name="名前")
    kyogleeid = models.IntegerField(verbose_name="期")
    joinyear = models.IntegerField(verbose_name="入団年")
    faculty = models.CharField(max_length=100, verbose_name="所属")
    part = models.CharField(max_length=10, choices=PART_CHOICES, verbose_name="パート")
    #role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name="役職")
    role = models.ManyToManyField(Role, verbose_name="役職", blank=True)
    #picture = models.ImageField(upload_to="member/picture/", blank=True, null=True, verbose_name="写真")
    picture = CloudinaryField('画像', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時") #そのデータがはじめて作られたそのときの日時を保存
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時") #データが保存・更新されるたびに記録
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True) #ログインUserとMemberの個人を紐付け
    
    def __str__(self):
        return self.name #判別に分かりやすいもの（.name）を指定
    
    @property
    def is_financial(self):
        return self.role.filter(code='Zaimu').exists()