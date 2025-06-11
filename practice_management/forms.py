# practice_management/forms.py

from django import forms
from .models import PracticeMonth, PracticeDay
from member.models import Member

class PracticeMonthCreateForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=Member.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="含める団員"
    )

    year = forms.ChoiceField(
        choices=[(y, f"{y}年") for y in range(2024, 2031)],
        label="年"
    )

    month = forms.ChoiceField(
        choices=[(m, f"{m}月") for m in range(1, 13)],
        label="月"
    )

    class Meta:
        model = PracticeMonth
        fields = ['year', 'month', 'members']


class PracticeDayDetailForm(forms.ModelForm):
    start_time = forms.TimeField(
        label="開始時刻",
        widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time'})
    )

    end_time = forms.TimeField(
        label="終了時刻",
        widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time'})
    )
    class Meta:
        model = PracticeDay
        fields = ['start_time', 'end_time', 'status', 'location', 'custom_location', 'content', 'note']
        labels = {
            'status': '種別',
            'location': '場所',
            'custom_location': '場所（その他）',
            'content': '内容',
            'note': '備考',
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'class': 'responsive-textarea'}),
            'note': forms.Textarea(attrs={'rows': 5, 'cols': 40, 'class': 'responsive-textarea'}),
            'custom_location': forms.TextInput(attrs={'placeholder': 'その他の場合のみ記入'}),
        }
