from django.db import models
from member.models import Member  # 団員モデルを参照
from django.utils import timezone

class ExpenseApplication(models.Model):
    APPROVAL_CHOICES = [
        ('pending', '申請中'),
        ('refunded', '承認'),
        ('rejected', '却下'),
    ]
    PAYMENT_CHOICES = [
        ('unpaid', '未払い'),
        ('paid', '払い済み'),
    ]
    applicant = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='expenses')
    description = models.CharField(max_length=255)
    amount = models.IntegerField(verbose_name="金額（円）")
    receipt_image = models.ImageField(upload_to='receipts/', blank=True, null=True)
    submitted_at = models.DateTimeField(default=timezone.now)
    #status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    approval_status = models.CharField(max_length=10, choices=APPROVAL_CHOICES, default='pending')
    payment_status = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='unpaid')
    def __str__(self):
        return f"{self.applicant} - {self.amount}円 - {self.approval_status} / {self.payment_status}"