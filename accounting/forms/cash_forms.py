from django import forms
from accounting.models.cash_models import CashPage, CashItem, CashBudget

# =============================
# 会計表（CashPage）作成用フォーム
# =============================
class CashPageForm(forms.ModelForm):
    class Meta:
        model = CashPage
        fields = ['year', 'title', 'notes', 'approval_status']
        labels = {
            'year': '年度',
            'title': '会計表名',
            'notes': '備考',
            'approval_status': '予算承認ステータス',
        }
        widgets = {
            'approval_status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 5, 'cols': 40, 'class': 'responsive-textarea'}),
        }

# =============================
# 予算入力フォーム（CashBudget）
# =============================
class CashBudgetForm(forms.ModelForm):
    class Meta:
        model = CashBudget
        exclude = ['cash_page']
        labels = {
            'member_fee': '団員徴収',
            'cash_savings': '現金／預金',
            'ticket': 'チケット売上',
            'ads': '広告',
            'donation': '寄付',
            'anniversary': '50周年基金',
            'income_other': 'その他（収入）',
            'facility': '施設／設備費',
            'venue': '会館使用料',
            'printing': '印刷費',
            'honorarium': '御礼',
            'food': '食費',
            'lodging': '宿泊費',
            'score': '楽譜',
            'misc': '雑費',
            'expense_other': 'その他（支出）',
        }
        widgets = {
            field: forms.NumberInput(attrs={'min': 0, 'class': 'form-control'})
            for field in model._meta.get_fields()
            if isinstance(field, forms.fields.Field) and field.name != 'cash_page'
        }

# =============================
# 出入金項目追加フォーム
# =============================
class CashItemForm(forms.ModelForm):
    SUBJECT_CHOICES = [
        ("団員徴収", "団員徴収"),
        ("現金／預金", "現金／預金"),
        ("チケット売上", "チケット売上"),
        ("広告", "広告"),
        ("寄付", "寄付"),
        ("50周年基金", "50周年基金"),
        ("その他（収入）", "その他（収入）"),
        ("施設／設備費", "施設／設備費"),
        ("会館使用料", "会館使用料"),
        ("印刷費", "印刷費"),
        ("御礼", "御礼"),
        ("食費", "食費"),
        ("宿泊費", "宿泊費"),
        ("楽譜", "楽譜"),
        ("雑費", "雑費"),
        ("その他（支出）", "その他（支出）"),
    ]

    subject = forms.ChoiceField(choices=SUBJECT_CHOICES, label="科目")

    class Meta:
        model = CashItem
        exclude = ['cash_page']
        labels = {
            'date': '日付',
            'cash_type': '収支区分',
            'subject': '科目',
            'description': '項目',
            'amount': '金額',
            'notes': '備考',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'cash_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'placeholder': '例：情宣チケット'}),
            'amount': forms.NumberInput(attrs={'min': 0}),
            'notes': forms.Textarea(attrs={'rows': 5, 'cols': 40, 'class': 'responsive-textarea'}),
        }
