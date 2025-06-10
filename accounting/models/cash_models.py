import uuid
from django.db import models

# ================================
# 会計表（年度ごとの予実＋出入金管理の単位）
# ================================
class CashPage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    year = models.PositiveIntegerField(verbose_name="年度")
    title = models.CharField(max_length=255, verbose_name="会計表名")
    notes = models.TextField(blank=True, verbose_name="備考")
    approval_status = models.CharField(
        max_length=20,
        choices=[('未承認', '未承認'), ('承認済み', '承認済み')],
        default='未承認',
        verbose_name="予算承認ステータス"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.year}年 - {self.title}"

# ================================
# 出入金項目（収支レコード）
# ================================
class CashItem(models.Model):
    CASH_TYPE_CHOICES = [('収入', '収入'), ('支出', '支出')]

    cash_page = models.ForeignKey(CashPage, on_delete=models.CASCADE, related_name='items')
    date = models.DateField(verbose_name="日付")
    cash_type = models.CharField(max_length=10, choices=CASH_TYPE_CHOICES, verbose_name="収支区分")
    subject = models.CharField(max_length=100, verbose_name="科目")  # チケット売上、御礼など
    description = models.CharField(max_length=255, verbose_name="項目")
    amount = models.PositiveIntegerField(verbose_name="金額")
    notes = models.TextField(blank=True, verbose_name="備考")

    def __str__(self):
        return f"{self.date} {self.cash_type} {self.description} - {self.amount}円"

# ================================
# 予算（科目別の予算入力データ）
# ================================
class CashBudget(models.Model):
    cash_page = models.OneToOneField(CashPage, on_delete=models.CASCADE, related_name='budget')

    # --- 収入科目 ---
    member_fee = models.PositiveIntegerField(default=0, verbose_name="団員徴収")
    cash_savings = models.PositiveIntegerField(default=0, verbose_name="現金／預金")
    ticket = models.PositiveIntegerField(default=0, verbose_name="チケット売上")
    ads = models.PositiveIntegerField(default=0, verbose_name="広告")
    donation = models.PositiveIntegerField(default=0, verbose_name="寄付")
    anniversary = models.PositiveIntegerField(default=0, verbose_name="50周年基金")
    income_other = models.PositiveIntegerField(default=0, verbose_name="その他（収入）")

    # --- 支出科目 ---
    facility = models.PositiveIntegerField(default=0, verbose_name="施設／設備費")
    venue = models.PositiveIntegerField(default=0, verbose_name="会館使用料")
    printing = models.PositiveIntegerField(default=0, verbose_name="印刷費")
    honorarium = models.PositiveIntegerField(default=0, verbose_name="御礼")
    food = models.PositiveIntegerField(default=0, verbose_name="食費")
    lodging = models.PositiveIntegerField(default=0, verbose_name="宿泊費")
    score = models.PositiveIntegerField(default=0, verbose_name="楽譜")
    misc = models.PositiveIntegerField(default=0, verbose_name="雑費")
    expense_other = models.PositiveIntegerField(default=0, verbose_name="その他（支出）")

    def __str__(self):
        return f"{self.cash_page.title} の予算"
