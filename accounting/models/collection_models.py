from django.db import models
from member.models import Member

class Collection(models.Model):
    title = models.CharField(max_length=255, verbose_name="徴収項目")
    content = models.TextField(verbose_name="徴収内容", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日")
    deadline = models.DateField(verbose_name="徴収期限日")

    def __str__(self):
        return f"{self.title}（{self.deadline}）"


class CollectionRecord(models.Model):
    STATUS_CHOICES = [
        ('未', '未'),
        ('済', '済'),
        ('不要', '不要'),
    ]
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='records')
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(verbose_name="徴収額", default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='未', verbose_name="徴収ステータス")

    def __str__(self):
        return f"{self.member.name} - {self.amount}円 - {self.status}"
