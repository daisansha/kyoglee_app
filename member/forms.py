from django.forms import ModelForm
from django import forms
from .models import Member, Role  # MemberモデルとRoleモデルをインポート

# =============================
# Member モデルに対応するフォーム定義
# =============================
# このフォームを使って、団員情報の登録・更新を行う
class MemberForm(ModelForm):
    class Meta:
        model = Member  # 対応するモデル
        fields = [
            "name",
            "kyogleeid",
            "joinyear",
            "faculty",
            "part",
            "role",
            "picture"
        ]  # フォームに表示させるフィールドを指定

        # 入力フォームの見た目・補助テキスト（プレースホルダーなど）
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': '例）小林一貴'}),
            'kyogleeid': forms.TextInput(attrs={'placeholder': '例）59'}),
            'joinyear': forms.TextInput(attrs={'placeholder': '例）2022'}),
            'faculty': forms.TextInput(attrs={'placeholder': '例）経済学部'}),
            'role': forms.CheckboxSelectMultiple,  # 複数選択をチェックボックスで表示
        }