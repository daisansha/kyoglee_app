# 画面表示・処理ロジックの中心
# クラスベースビューを使用し、ログイン必須（LoginRequiredMixin）

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View #View用の基底クラス
from .forms import MemberForm #forms.pyのMemberFormクラスをインポートし継承
from .models import Member
from datetime import datetime
from zoneinfo import ZoneInfo
from practice_management.models import PracticeAttendance, PracticeDay  # 上部に追加
from collections import defaultdict
from django.contrib.auth.decorators import login_required
from accounting.models.collection_models import CollectionRecord  # 追加

#トップページにアクセスしたときの処理
class IndexView(LoginRequiredMixin,View):
    def get(self, request):
        datetime_now = datetime.now(
            ZoneInfo("Asia/Tokyo")
        ).strftime("%Y年%m月%d日 %H:%M:%S")
        return render(request, "member/index.html", {"datetime_now":datetime_now}) #render:リスポンスとして画面を返す

#入力画面にアクセスしたときの処理　入力画面の表示と入力内容の保存
class MemberCreateView(LoginRequiredMixin,View): #Djangoの View クラスを継承して、**HTTPリクエストに応じた処理（get, postなど）**を定義する。LoginRequiredMixin を使うことで、ログインしていないユーザーをログインページにリダイレクトさせる（認証機能）。

    def get(self, request): #GET リクエスト（ページにアクセス）してきたときの処理。
        form = MemberForm() # 空の入力フォームを生成。
        return render(request, "member/member_form.html", {"form": form}) # "member/member_form.html" というテンプレートを表示し、フォームを渡す。member_form.htmlのform.as_pとつなげ、アクセスしたときに処理が行われるようにする。
    
    def post(self, request): #フォームを送信（POST） したときの処理。
        form = MemberForm(request.POST, request.FILES) #MemberForm(...) に request.POST（テキスト等）と request.FILES（画像等）を渡す。
        if form.is_valid(): #form.is_valid() でバリデーション（必須入力・型チェックなど）を実行。
            form.save() # 成功したらform.save() でDBに保存し、トップページへリダイレクト。
            return redirect("member:index")
        return render(request, "member/member_form.html", {"form":form}) #失敗したら、同じフォームを再表示（エラー付き）。

#一覧画面
class MemberListView(LoginRequiredMixin,View):
    def get(self, request):
        member_list = Member.objects.order_by("kyogleeid")
        return render(request, "member/member_list.html", {"member_list":member_list})

#詳細画面
class MemberDetailView(LoginRequiredMixin, View):
    def get(self, request, id):
        member = get_object_or_404(Member, id=id)
        form = MemberForm(instance=member)
        for field in form.fields.values():
            field.disabled = True

        # 📌 月別の出席数／予定数を集計
        attendance_records = PracticeAttendance.objects.select_related("day").filter(member=member)
        
        # 📌 徴収記録を取得（関連する Collection 情報も含めて）
        collection_records = CollectionRecord.objects.select_related('collection')\
            .filter(member=member).order_by('-collection__deadline')
        
        monthly_stats = defaultdict(lambda: {"attended": 0, "total": 0})  # {(year, month): {...}}

        for att in attendance_records:
            year = att.day.date.year
            month = att.day.date.month
            if att.day.status != "none":  # 「なし」は予定数に含めない
                monthly_stats[(year, month)]["total"] += 1
                if att.status in ["present", "late"]:
                    monthly_stats[(year, month)]["attended"] += 1

        # 📅 表示用に並べ替え（降順）
        sorted_stats = sorted(monthly_stats.items(), reverse=True)

        return render(request, "member/member_detail.html", {
            "member": member,
            "form": form,
            "monthly_attendance": sorted_stats,  # ← 
            "collection_records": collection_records,  # ← 追加
        })

#更新画面
class MemberUpdateView(LoginRequiredMixin,View):
    def get(self, request, id):
        member = get_object_or_404(Member, id=id) #対象のデータを取得
        #print("FILES:", request.FILES) 
        form = MemberForm(instance=member) #元のデータを初期値とする
        return render(request, "member/member_update.html", {"form":form})
    
    def post(self, request, id):
        member = get_object_or_404(Member, id=id)
        form = MemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            return redirect("member:member_detail", id=id)
        return render(request, "member/member_form.html", {"form":form})
        #redirect(...) → 別のURLに「移動」
        #render(...) → 同じテンプレートを「再表示（再レンダリング）」

@login_required
def delete_member(request, id):
    member = get_object_or_404(Member, id=id)

    if request.method == 'POST':
        member.delete()
        return redirect('member:member_list')

    return render(request, 'member/member_confirm_delete.html', {
        'member': member
    })

# 最後に as_view() で関数として urls.py に渡せるようにしている。
index = IndexView.as_view() #IndexViewクラスをas_view()メソッドで関数に変換し、代入
member_create = MemberCreateView.as_view() 
#クラスベースビュー（MemberCreateView）を 関数として扱えるように変換するもの。
#Djangoの urls.py は関数形式でビューを指定するため、as_view() が必要。
member_list = MemberListView.as_view()
member_detail = MemberDetailView.as_view()
member_update = MemberUpdateView.as_view()
