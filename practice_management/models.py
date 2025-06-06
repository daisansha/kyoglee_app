# practice_management/models.py

from django.db import models
from datetime import time
from member.models import Member

class PracticeMonth(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    members = models.ManyToManyField(Member)

    def __str__(self):
        return f"{self.year}年{self.month}月"

class PracticeDay(models.Model):
    month = models.ForeignKey(PracticeMonth, on_delete=models.CASCADE, related_name="days",
    null=True,        # ← 一時的に追加
    blank=True        # ← 一時的に追加
    )
    date = models.DateField() #unique=Trueマイグレーション時外す

    # 追加または修正
    start_time = models.TimeField(default=time(18, 30))
    end_time = models.TimeField(default=time(21, 0))

    STATUS_CHOICES = [
        ('practice', '練習'),
        ('matsuoka_practice', '松岡練習'),
        ('motoyama_practice', '本山練習'),
        ('piano_practice', 'ピアノ練習'),
        ('concert', '演奏会'),
        ('welcome', '新歓'),
        ('training_camp', '合宿'),
        ('none', 'なし'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='none')

    LOCATION_CHOICES = [
        ('地塩寮', '地塩寮'),
        ('２階共用室', '２階共用室'),
        ('２階和室', '２階和室'),
        ('地下共用室', '地下共用室'),
        ('4共20', '4共20'),
        ('4共21', '4共21'),
        ('4共30', '4共30'),
        ('4共31', '4共31'),
        ('4共40', '4共40'),
        ('BOX', 'BOX'),
        ('日仏会館', '日仏会館'),
        ('その他', 'その他'),
        ('-', '-'),
    ]
    location = models.CharField(max_length=100, choices=LOCATION_CHOICES, default='-')
    custom_location = models.CharField(max_length=100, blank=True)

    # 内容・備考
    content = models.TextField(blank=True)  
    note = models.TextField(blank=True)

    # 先生：チェックボックス → JSONFieldに変換
    teachers = models.JSONField(default=list, blank=True)  # ["松岡先生", "伴奏の先生", ...]

    def __str__(self):
        return f"{self.date} の練習"

class PracticeAttendance(models.Model):
    day = models.ForeignKey(PracticeDay, on_delete=models.CASCADE, related_name="attendances")
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    ATTENDANCE_CHOICES = [
        ('present', '〇'),
        ('late', '△'),
        ('absent', '✕'),
        ('undecided', 'ー'),
    ]
    status = models.CharField(max_length=10, choices=ATTENDANCE_CHOICES, default='undecided')

    def __str__(self):
        return f"{self.day} - {self.member} - {self.status}"
    
    class Meta:
        unique_together = ('day', 'member')  # ← ★ここを追加！
    