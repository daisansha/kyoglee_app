from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounting.models.cash_models import CashPage, CashBudget, CashItem
from accounting.forms.cash_forms import CashPageForm, CashBudgetForm, CashItemForm
from collections import defaultdict
from django.db.models import Sum
from django.contrib import messages
from django.utils.timezone import now

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
# 会計表詳細
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
    # income_total = income_items.aggregate(Sum('amount'))['amount__sum'] or 0
    # expense_total = expense_items.aggregate(Sum('amount'))['amount__sum'] or 0
    # balance = income_total - expense_total

    # 実費（subjectごとの合計）
    actuals = defaultdict(int)
    for item in items:
        actuals[item.subject] += item.amount

    # budget フィールド一覧（テンプレートで _meta.fields を避けるため）
    budget_fields = []
    if budget:
        for field in CashBudget._meta.fields:
            if field.name not in ('id', 'cash_page'):
                label = field.verbose_name
                value = getattr(budget, field.name)
                budget_fields.append((label, value))

    # ▼ 集計追加：予算・実費の小計および差額を算出
    income_labels = [
        "団員徴収", "現金／預金", "チケット売上", "広告",
        "寄付", "50周年基金", "その他（収入）"
    ]
    expense_labels = [
        "施設／設備費", "会館使用料", "印刷費", "御礼",
        "食費", "宿泊費", "楽譜", "雑費", "その他（支出）"
    ]

    # budget_values: {ラベル: 予算}
    #budget_values = dict(budget_fields)
    budget_values = {label: value for (label, value) in budget_fields}

    return render(request, 'accounting/cash/cash_page.html', {
        'cash_page': cash_page,
        'budget': budget,
        'budget_fields': budget_fields,  # ← 新たに追加されたcontext
        'income_items': income_items,
        'expense_items': expense_items,
        #'income_total': income_total,
        #'expense_total': expense_total,
        #'balance': balance,
        'actuals': dict(actuals),
        'budget_values': budget_values,
        'income_labels': income_labels,
        'expense_labels': expense_labels,
    })

# ================================
# 予実管理表更新
# ================================
@login_required
def cash_plan_update(request, pk):
    cash_page = get_object_or_404(CashPage, pk=pk)
    budget = getattr(cash_page, 'budget', None)

    if not budget:
        messages.error(request, "この会計表には予算が設定されていません。")
        return redirect('accounting:cash_page', pk=pk)

    if request.method == 'POST':
        form = CashBudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()

            # 🔽 approval_status だけ直接処理（formを使わず手動で保存）
            approval_value = request.POST.get("approval_status")
            if approval_value in dict(CashPage._meta.get_field("approval_status").choices):
                cash_page.approval_status = approval_value
                cash_page.save()

            messages.success(request, f"予算を更新しました（{now().strftime('%Y/%m/%d %H:%M')}）")
            return redirect('accounting:cash_page', pk=pk)
    else:
        form = CashBudgetForm(instance=budget)

    return render(request, 'accounting/cash/cash_plan_update.html', {
        'cash_page': cash_page,
        'form': form,
    })

# ================================
# 出入金管理表項目追加
# ================================    
@login_required
def cash_item_add(request, pk):
    cash_page = get_object_or_404(CashPage, pk=pk)

    if request.method == 'POST':
        form = CashItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.cash_page = cash_page
            item.save()
            messages.success(request, "項目を追加しました。")
            return redirect('accounting:cash_page', pk=pk)
    else:
        form = CashItemForm()

    return render(request, 'accounting/cash/cash_item_add.html', {
        'cash_page': cash_page,
        'form': form,
    })

# ================================
# 出入金管理表項目詳細
# ================================ 
@login_required
def cash_item_detail(request, pk, item_id):
    cash_page = get_object_or_404(CashPage, pk=pk)
    item = get_object_or_404(CashItem, id=item_id, cash_page=cash_page)

    if request.method == 'POST':
        form = CashItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "項目を更新しました。")
            return redirect('accounting:cash_page', pk=pk)
    else:
        form = CashItemForm(instance=item)

    return render(request, 'accounting/cash/cash_item_detail.html', {
        'cash_page': cash_page,
        'form': form,
        'item': item,
    })

# ================================
# 出入金管理表項目削除
# ================================
@login_required
def cash_item_delete(request, pk, item_id):
    cash_page = get_object_or_404(CashPage, pk=pk)
    item = get_object_or_404(CashItem, id=item_id, cash_page=cash_page)

    if request.method == 'POST':
        item.delete()
        messages.success(request, "項目を削除しました。")
        return redirect('accounting:cash_page', pk=pk)

    return render(request, 'accounting/cash/cash_item_delete.html', {
        'cash_page': cash_page,
        'item': item,
    })

# ================================
# 会計表削除
# ================================
@login_required
def cash_page_delete(request, pk):
    cash_page = get_object_or_404(CashPage, pk=pk)

    if request.method == 'POST':
        cash_page.delete()  # related_name のおかげで budget, items も削除される
        messages.success(request, f"会計表「{cash_page.title}」を削除しました。")
        return redirect('accounting:cash_page_list')

    return render(request, 'accounting/cash/cash_page_delete.html', {
        'cash_page': cash_page,
    })
