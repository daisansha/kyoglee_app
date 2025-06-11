from django import forms
from django.forms import modelformset_factory
from accounting.models.collection_models import Collection, CollectionRecord
from member.models import Member

# ======================================
# 徴収項目作成用フォーム
# （タイトル、内容、期限）
# ======================================
class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['title', 'content', 'deadline']
        labels = {
            'title': '徴収項目',
            'content': '徴収内容詳細',
            'deadline': '徴収期限日',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '例）2025年度前期団費'}),
            'content': forms.TextInput(attrs={'rows': 5, 'cols': 40, 'class': 'responsive-textarea'}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),  # 日付選択用カレンダー入力
        }

# ======================================
# 個別の徴収レコード編集用フォーム
# （対象団員はreadonly）
# ======================================
class CollectionRecordForm(forms.ModelForm):
    class Meta:
        model = CollectionRecord
        fields = ['member', 'amount', 'status']
        labels = {
            'member': '団員',
            'amount': '徴収額',
            'status': '徴収',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 団員は割り当て済みのものを表示専用に
        self.fields['member'].disabled = True

# ======================================
# 複数の徴収記録（団員ごと）を一括管理するFormSet
# ======================================
CollectionRecordFormSet = modelformset_factory(
    CollectionRecord,
    form=CollectionRecordForm,
    extra=0,          # 既存レコードのみ表示
    can_delete=False  # レコードの削除はフォーム上では不可
)