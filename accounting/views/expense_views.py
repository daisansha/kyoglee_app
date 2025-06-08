from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from accounting.models.expense_models import ExpenseApplication
from accounting.forms.expense_forms import ExpenseApplicationForm

# ===============================
# 会計機能トップページ（ダッシュボード）
# ===============================
@login_required
def accounting_index(request):
    return render(request, 'accounting/index.html')

# ===============================
# 経費申請（新規）フォーム表示と登録
# ===============================
@login_required 
def expense_apply(request):
    if request.method == 'POST':
        form = ExpenseApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.applicant = request.user.member  # ログインユーザーに紐づく団員情報を自動設定
            expense.save()
            return redirect('accounting:expense_list')
    else:
        form = ExpenseApplicationForm()
    return render(request, 'accounting/expense/apply.html', {'form': form})

# ===============================
# 経費申請一覧（全申請を表示）
# ===============================
@login_required
def expense_list(request):
    expense_list = ExpenseApplication.objects.all().order_by('-submitted_at')
    return render(request, 'accounting/expense/list.html', {'expense_list': expense_list})

# ===============================
# 経費申請詳細（表示専用フォーム、全フィールド無効化）
# ===============================
@login_required
def expense_detail(request, id):
    expense = get_object_or_404(ExpenseApplication, id=id)
    form = ExpenseApplicationForm(instance=expense)
    for field in form.fields.values():
        field.disabled = True  # フォーム項目をすべて読み取り専用に
    return render(request, 'accounting/expense/detail.html', {
        'expense': expense,
        'form': form,
    })

# ===============================
# 経費申請の編集（財務以外は承認・支払ステータスを編集不可に）
# ===============================
@login_required
def expense_update(request, id):
    expense = get_object_or_404(ExpenseApplication, id=id)

    if request.method == 'POST':
        form = ExpenseApplicationForm(request.POST, request.FILES, instance=expense)
        if form.is_valid():
            if not request.user.member.is_financial:
                # 財務でないユーザーが送信した場合、ステータスを変更させない
                form.cleaned_data['approval_status'] = expense.approval_status
                form.cleaned_data['payment_status'] = expense.payment_status
            form.save()
            return redirect('accounting:expense_detail', id=expense.id)
    else:
        form = ExpenseApplicationForm(instance=expense)
        if not request.user.member.is_financial:
            for field in ['approval_status', 'payment_status']:
                form.fields[field].disabled = True

    return render(request, 'accounting/expense/update.html', {
        'form': form,
        'expense': expense,
    })

# ===============================
# 経費申請の削除（確認画面 → 実行）
# ===============================
@login_required
def expense_delete(request, id):
    expense = get_object_or_404(ExpenseApplication, id=id)

    if request.method == 'POST':
        expense.delete()
        return redirect('accounting:expense_list')

    form = ExpenseApplicationForm(instance=expense)
    for field in form.fields.values():
        field.disabled = True

    return render(request, 'accounting/expense/delete.html', {
        'form': form,
        'expense': expense,
    })