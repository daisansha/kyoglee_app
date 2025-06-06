from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
#from .models import ExpenseApplication
#from .forms import ExpenseApplicationForm
from accounting.models.expense_models import ExpenseApplication
from accounting.forms.expense_forms import ExpenseApplicationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def accounting_index(request):
    return render(request, 'accounting/index.html') #会計ホームページ表示用ビュー

@login_required 
def expense_apply(request): #経費申請（POSTで保存、GETでフォーム表示）
    if request.method == 'POST':
        form = ExpenseApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.applicant = request.user.member  # ログインユーザーの団員情報を参照（要調整）
            expense.save()
            return redirect('accounting:expense_list')  # 完了後一覧へリダイレクト
    else:
        form = ExpenseApplicationForm()
    return render(request, 'accounting/expense/apply.html', {'form': form})

@login_required
def expense_list(request): #ログインユーザーの申請一覧
    # ログインユーザーの Member に紐づく申請だけ取得
    expense_list = ExpenseApplication.objects.all().order_by('-submitted_at')
    return render(request, 'accounting/expense/list.html', {'expense_list': expense_list})

@login_required
def expense_detail(request, id): #フォーム表示＋全項目 disabled=True（＝表示専用として最適）
    expense = get_object_or_404(ExpenseApplication, id=id)
    
    # フォームは作るが、フィールドをすべて disabled にする
    form = ExpenseApplicationForm(instance=expense)
    for field in form.fields.values():
        field.disabled = True

    return render(request, 'accounting/expense/detail.html', {
        'expense': expense,
        'form': form,
    })

def expense_update(request, id):
    expense = get_object_or_404(ExpenseApplication, id=id)

    if request.method == 'POST':
        form = ExpenseApplicationForm(request.POST, request.FILES, instance=expense)
        if form.is_valid():
            if not request.user.member.is_financial:
                # 財務でない場合、承認・支払ステータスは変更させない
                form.cleaned_data['approval_status'] = expense.approval_status
                form.cleaned_data['payment_status'] = expense.payment_status
            form.save()
            return redirect('accounting:expense_detail', id=expense.id)
    else:
        form = ExpenseApplicationForm(instance=expense)

        # 財務でなければフィールドをロック
        if not request.user.member.is_financial:
            for field in ['approval_status', 'payment_status']:
                form.fields[field].disabled = True

    return render(request, 'accounting/expense/update.html', {'form': form, 'expense': expense})

@login_required
def expense_delete(request, id):
    expense = get_object_or_404(ExpenseApplication, id=id)

    if request.method == 'POST':
        expense.delete()
        return redirect('accounting:expense_list')

    # フォームを作成し、すべてのフィールドをdisabledに
    form = ExpenseApplicationForm(instance=expense)
    for field in form.fields.values():
        field.disabled = True

    return render(request, 'accounting/expense/delete.html', {
        'form': form,
        'expense': expense,
    })
