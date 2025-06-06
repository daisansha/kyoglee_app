# practice_management/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PracticeMonthCreateForm, PracticeDayDetailForm
from .models import PracticeMonth, PracticeDay
from calendar import monthrange
from datetime import date
from .models import PracticeMonth, PracticeDay, PracticeAttendance
from member.models import Member

@login_required
def practice_index(request):
    months = PracticeMonth.objects.order_by('year', 'month')
    return render(request, 'practice_management/practice_index.html', {
        'months': months
    })

@login_required
def create_practice_record(request):
    if request.method == 'POST':
        form = PracticeMonthCreateForm(request.POST)
        if form.is_valid():
            month_record = form.save()
            year = month_record.year
            month = month_record.month
            days_in_month = monthrange(year, month)[1]

            for day in range(1, days_in_month + 1):
                PracticeDay.objects.create(
                    month=month_record,
                    date=date(year, month, day)
                )

            return redirect('practice_management:practice_record', year=year, month=month)
    else:
        form = PracticeMonthCreateForm()

    return render(request, 'practice_management/create_practice_record.html', {
        'form': form
    })

@login_required
def practice_record(request, year, month):
    practice_month = get_object_or_404(PracticeMonth, year=year, month=month)
    days = practice_month.days.order_by('date')
    members = practice_month.members.order_by('kyogleeid', 'name')

    if request.method == "POST":
        for day in days:
            # 練習予定ステータス（例: 演奏会など）
            status_key = f"status_{day.id}"
            if status_key in request.POST:
                day.status = request.POST[status_key]
            # 場所保存
            location_key = f"location_{day.id}"
            if location_key in request.POST:
                day.location = request.POST[location_key]
            day.save()

            for member in members:
                att_key = f"att_{day.id}_{member.id}"
                if att_key in request.POST:
                    attendance, created = PracticeAttendance.objects.get_or_create(
                        day=day, member=member
                    )
                    attendance.status = request.POST[att_key]
                    attendance.save()

        return redirect("practice_management:practice_record", year=year, month=month)

    # ✅ 修正：keyをテンプレートと一致させる（"att_dayid_memberid"）
    attendance_dict = {}
    for a in PracticeAttendance.objects.filter(day__in=days, member__in=members):
        key = f"att_{str(a.day_id)}_{str(a.member_id)}"
        attendance_dict[key] = {
            "status": str(a.status),  # ← 強制的に文字列化（"present"など）
            "choices": PracticeAttendance.ATTENDANCE_CHOICES
        }
        
    # ✅ ここから追加：行・列ごとの出席集計
    row_totals = {}  # 各日ごとの出席者数
    col_totals = {}  # 各メンバーごとの出席日数

    for member in members:
        col_totals[member.id] = 0

    for day in days:
        count = 0
        for member in members:
            key = f"att_{day.id}_{member.id}"
            status = attendance_dict.get(key, {}).get("status", "undecided")
            if status in ["present", "late"]:
                count += 1
                col_totals[member.id] += 1
        row_totals[day.id] = count        
        
    return render(request, 'practice_management/practice_record.html', {
        'practice_month': practice_month,
        'days': days,
        'members': members,
        'attendance_dict': attendance_dict,
        'row_totals': row_totals,
        'col_totals': col_totals,
    })

@login_required
def practice_record_detail(request, year, month, day):
    date_obj = date(year, month, day)
    practice_day = get_object_or_404(PracticeDay, date=date_obj)

    if request.method == 'POST':
        form = PracticeDayDetailForm(request.POST, instance=practice_day)
        if form.is_valid():
            form.save()
            return redirect('practice_management:practice_record', year=year, month=month)
    else:
        form = PracticeDayDetailForm(instance=practice_day)
        
    # ✅ ここから追加：出席ステータス分類
    attendances = PracticeAttendance.objects.filter(day=practice_day).select_related('member')
    participants = [a.member for a in attendances if a.status in ['present', 'late']]
    absentees = [a.member for a in attendances if a.status == 'absent']
    
    return render(request, 'practice_management/practice_record_detail.html', {
        'practice_day': practice_day,
        'form': form,
        'participants': participants,
        'absentees': absentees,
    })

@login_required
def delete_practice_month(request, year, month):
    practice_month = get_object_or_404(PracticeMonth, year=year, month=month)

    if request.method == 'POST':
        practice_month.delete()
        return redirect('practice_management:practice_index')

    return render(request, 'practice_management/practice_month_confirm_delete.html', {
        'practice_month': practice_month
    })
