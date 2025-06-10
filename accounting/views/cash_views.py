from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounting.models.cash_models import CashPage, CashBudget, CashItem
from accounting.forms.cash_forms import CashPageForm, CashBudgetForm, CashItemForm
from collections import defaultdict
from django.db.models import Sum

# ================================
# 会計表作成
# ================================
@login_required
def cash_page_create(request):
    if request.method == 'POST':
        page_form = CashPageForm(request.POST)
        budget_form = CashBudgetForm(request.POST)
        if page_form.is_valid() and budget_form.is_valid():
            cash_page = page_form.save()
            budget = budget_form.save(commit=False)
            budget.cash_page = cash_page
            budget.save()
            return redirect('accounting:cash_page_list')
    else:
        page_form = CashPageForm()
        budget_form = CashBudgetForm()

    return render(request, 'accounting/cash/cash_page_create.html', {
        'page_form': page_form,
        'budget_form': budget_form,
    })

# ================================
# 会計表一覧
# ================================
@login_required
def cash_page_list(request):
    pages = CashPage.objects.all().order_by('-year', 'title')
    return render(request, 'accounting/cash/cash_page_list.html', {
        'pages': pages
    })

# ================================
# 会計表
# ================================
@login_required
def cash_page(request, pk):
    cash_page = get_object_or_404(CashPage, pk=pk)
    budget = getattr(cash_page, 'budget', None)
    items = CashItem.objects.filter(cash_page=cash_page).order_by('date')

    # 収支分類
    income_items = items.filter(cash_type='収入')
    expense_items = items.filter(cash_type='支出')

    # 合計計算
    income_total = income_items.aggregate(Sum('amount'))['amount__sum'] or 0
    expense_total = expense_items.aggregate(Sum('amount'))['amount__sum'] or 0
    balance = income_total - expense_total

    # 実費計算（subjectごとに合計）
    actuals = defaultdict(int)
    for item in items:
        actuals[item.subject] += item.amount

    return render(request, 'accounting/cash/cash_page.html', {
        'cash_page': cash_page,
        'budget': budget,
        'income_items': income_items,
        'expense_items': expense_items,
        'income_total': income_total,
        'expense_total': expense_total,
        'balance': balance,
        'actuals': dict(actuals),
    })
