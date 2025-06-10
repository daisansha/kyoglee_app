from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounting.models.cash_models import CashPage, CashBudget, CashItem
from accounting.forms.cash_forms import CashPageForm, CashBudgetForm, CashItemForm

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
