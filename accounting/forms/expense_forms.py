from django import forms
from accounting.models.expense_models import ExpenseApplication
#from .models import ExpenseApplication
from member.models import Member

class ExpenseApplicationForm(forms.ModelForm):
    class Meta:
        model = ExpenseApplication
        fields = ['applicant', 'description', 'amount', 'approval_status', 'payment_status', 'receipt_image', ]
        labels = {
            'applicant': '申請者',
            'description': '申請理由',
            'amount': '金額',
            'approval_status': '承認ステータス',
            'payment_status': '支払いステータス',
            'receipt_image': '領収書',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # applicantフィールドに全てのMemberを明示的に設定（←重要）
        self.fields['applicant'].queryset = Member.objects.all()