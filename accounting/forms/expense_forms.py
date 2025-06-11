from django import forms
from accounting.models.expense_models import ExpenseApplication
from member.models import Member

# ============================================
# 経費申請モデルに対応するフォームクラス
# ============================================
class ExpenseApplicationForm(forms.ModelForm):
    class Meta:
        model = ExpenseApplication  # 対象モデル
        fields = [
            'applicant',
            'title',
            'description',
            'amount',
            'approval_status',
            'payment_status',
            'receipt_image',
        ]  # フォームに含めるフィールド

        labels = {
            'applicant': '申請者',
            'title': '申請項目',
            'description': '申請内容詳細',
            'amount': '金額',
            'approval_status': '承認ステータス',
            'payment_status': '支払いステータス',
            'receipt_image': '領収書',
        }  # フィールド名の日本語ラベル設定
        
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '例）新入生奢り（キャラバン）'}),
            'description': forms.TextInput(attrs={'rows': 5, 'cols': 40, 'class': 'responsive-textarea'}),
            'amount': forms.NumberInput(attrs={'min': 0}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 申請者フィールドに登録済み団員（Member）を全件セット
        self.fields['applicant'].queryset = Member.objects.all()
