#リクエストで受け取ったデータのバリュエーション、データの型変換を行う
from django.forms import ModelForm
from django import forms
from .models import Member, Role #.modelsのMemberクラスをインポート

class MemberForm(ModelForm):
    class Meta:
        model = Member
        fields = ["name","kyogleeid","joinyear","faculty","part","role","picture"] #ここが、入力画面に反映
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': '例）小林一貴'}),
            'kyogleeid': forms.TextInput(attrs={'placeholder': '例）59'}),
            'joinyear': forms.TextInput(attrs={'placeholder': '例）2022'}),
            'faculty': forms.TextInput(attrs={'placeholder': '例）経済学部'}),
            "role": forms.CheckboxSelectMultiple,
        }