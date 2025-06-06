from django import forms
from django.forms import modelformset_factory
from accounting.models.collection_models import Collection, CollectionRecord
from member.models import Member

class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['title', 'content', 'deadline']
        labels = {
            'title': '徴収項目',
            'content': '徴収内容',
            'deadline': '徴収期限日',
        }
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }

class CollectionRecordForm(forms.ModelForm):
    class Meta:
        model = CollectionRecord
        fields = ['member', 'amount', 'status']
        labels = {
            'member': '団員',
            'amount': '徴収額（円）',
            'status': '徴収ステータス',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['member'].disabled = True  # 団員名は編集不可に

CollectionRecordFormSet = modelformset_factory(
    CollectionRecord,
    form=CollectionRecordForm,
    extra=0,
    can_delete=False
)
