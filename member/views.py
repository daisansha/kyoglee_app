from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from .forms import MemberForm
from .models import Member
from datetime import datetime
from zoneinfo import ZoneInfo
from practice_management.models import PracticeAttendance, PracticeDay
from collections import defaultdict
from accounting.models.collection_models import CollectionRecord

# ===============================
# トップページビュー（ダッシュボード）
# ===============================
class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        datetime_now = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y年%m月%d日 %H:%M:%S")
        return render(request, "member/index.html", {"datetime_now": datetime_now})

# ===============================
# 団員新規登録（GET:フォーム表示 / POST:登録処理）
# ===============================
class MemberCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = MemberForm()
        return render(request, "member/member_form.html", {"form": form})

    def post(self, request):
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("member:index")
        return render(request, "member/member_form.html", {"form": form})

# ===============================
# 団員一覧表示
# ===============================
class MemberListView(LoginRequiredMixin, View):
    def get(self, request):
        sort_key = request.GET.get('sort')
        if sort_key in ['name', 'kyogleeid', 'joinyear', 'part', 'faculty', 'role']:
            member_list = Member.objects.all().order_by(sort_key)
        else:
            member_list = Member.objects.all()
        return render(request, "member/member_list.html", {"member_list": member_list})

# ===============================
# 団員詳細表示（出席情報・徴収情報を含む）
# ===============================
class MemberDetailView(LoginRequiredMixin, View):
    def get(self, request, id):
        member = get_object_or_404(Member, id=id)
        form = MemberForm(instance=member)
        for field in form.fields.values():
            field.disabled = True  # 表示のみで編集不可に

        # 出席記録の月別集計
        attendance_records = PracticeAttendance.objects.select_related("day").filter(member=member)
        monthly_stats = defaultdict(lambda: {"attended": 0, "total": 0})

        for att in attendance_records:
            year, month = att.day.date.year, att.day.date.month
            if att.day.status != "none":
                monthly_stats[(year, month)]["total"] += 1
                if att.status in ["present", "late"]:
                    monthly_stats[(year, month)]["attended"] += 1

        sorted_stats = sorted(monthly_stats.items(), reverse=True)

        # 徴収記録の取得（最新順）
        collection_records = CollectionRecord.objects.select_related('collection')\
            .filter(member=member).order_by('-collection__deadline')

        return render(request, "member/member_detail.html", {
            "member": member,
            "form": form,
            "monthly_attendance": sorted_stats,
            "collection_records": collection_records,
        })

# ===============================
# 団員情報の編集
# ===============================
class MemberUpdateView(LoginRequiredMixin, View):
    def get(self, request, id):
        member = get_object_or_404(Member, id=id)
        form = MemberForm(instance=member)
        return render(request, "member/member_update.html", {"form": form})

    def post(self, request, id):
        member = get_object_or_404(Member, id=id)
        form = MemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            return redirect("member:member_detail", id=id)
        return render(request, "member/member_form.html", {"form": form})

# ===============================
# 団員の削除（確認画面 → 実行）
# ===============================
@login_required
def delete_member(request, id):
    member = get_object_or_404(Member, id=id)
    if request.method == 'POST':
        member.delete()
        return redirect('member:member_list')
    return render(request, 'member/member_confirm_delete.html', {'member': member})

# ===============================
# 各クラスベースビューを関数化してURLに渡す
# ===============================
index = IndexView.as_view()
member_create = MemberCreateView.as_view()
member_list = MemberListView.as_view()
member_detail = MemberDetailView.as_view()
member_update = MemberUpdateView.as_view()