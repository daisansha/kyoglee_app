from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounting.models.collection_models import Collection, CollectionRecord
from accounting.forms.collection_forms import CollectionForm, CollectionRecordForm, CollectionRecordFormSet
from member.models import Member

# ===============================
# 会計アプリのトップページ
# ===============================
@login_required
def accounting_index(request):
    return render(request, 'accounting/index.html')

# ===============================
# 徴収項目の新規作成 + 団員別の徴収記録も同時作成
# ===============================
@login_required
def collection_create(request):
    members = Member.objects.all().order_by('kyogleeid', 'name')
    kyoglee_list = Member.objects.values_list('kyogleeid', flat=True).distinct().order_by('kyogleeid')

    if request.method == 'POST':
        form = CollectionForm(request.POST)
        record_forms = []

        all_valid = True
        for member in members:
            amount_key = f"amount_{member.id}"
            status_key = f"status_{member.id}"

            try:
                amount = int(request.POST.get(amount_key, 0))
                status = request.POST.get(status_key, '未')
            except ValueError:
                amount = 0
                status = '未'

            if status == '不要':
                amount = 0

            record_forms.append({
                'member': member,
                'amount': amount,
                'status': status,
            })

        if form.is_valid():
            collection = form.save()
            for record in record_forms:
                CollectionRecord.objects.create(
                    collection=collection,
                    member=record['member'],
                    amount=record['amount'],
                    status=record['status']
                )
            return redirect('accounting:collection_list', year=collection.deadline.year)

    else:
        form = CollectionForm()
        record_forms = [{'member': m, 'amount': '', 'status': '未'} for m in members]

    return render(request, 'accounting/collection/collection_create.html', {
        'form': form,
        'members': members,
        'record_forms': record_forms,
        'kyoglee_list': kyoglee_list,
    })

# ===============================
# 年ごとの徴収一覧とステータス集計
# ===============================
@login_required
def collection_list(request, year):
    collections = Collection.objects.filter(deadline__year=year).order_by('deadline')

    collection_info = []
    for col in collections:
        records = col.records.all()
        total = records.exclude(status="不要").count()
        done = records.filter(status="済").count()
        pending = records.filter(status="未").values_list('member__name', flat=True)

        collection_info.append({
            'collection': col,
            'done_count': done,
            'total_count': total,
            'pending_members': list(pending),
        })

    return render(request, 'accounting/collection/collection_list.html', {
        'year': year,
        'collection_info': collection_info,
    })

# ===============================
# 徴収項目の詳細（全フィールド readonly 表示）
# ===============================
@login_required
def collection_detail(request, year, pk):
    collection = get_object_or_404(Collection, pk=pk)
    form = CollectionForm(instance=collection)
    for field in form.fields.values():
        field.disabled = True

    records = CollectionRecord.objects.filter(collection=collection)\
        .select_related('member').order_by('member__kyogleeid', 'member__name')

    return render(request, 'accounting/collection/collection_detail.html', {
        'form': form,
        'collection': collection,
        'records': records,
    })

# ===============================
# 徴収項目と個別徴収記録の更新
# ===============================
@login_required
def collection_update(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    members = Member.objects.all().order_by('kyogleeid', 'name')
    existing_records = {r.member.id: r for r in CollectionRecord.objects.filter(collection=collection)}

    if request.method == 'POST':
        form = CollectionForm(request.POST, instance=collection)

        if form.is_valid():
            form.save()

            for member in members:
                amount_key = f"amount_{member.id}"
                status_key = f"status_{member.id}"

                try:
                    amount = int(request.POST.get(amount_key, 0))
                    status = request.POST.get(status_key, '未')
                except ValueError:
                    amount = 0
                    status = '未'

                if status == '不要':
                    amount = 0

                record = existing_records.get(member.id)
                if record:
                    record.amount = amount
                    record.status = status
                    record.save()

            return redirect('accounting:collection_detail', year=collection.deadline.year, pk=collection.id)

    else:
        form = CollectionForm(instance=collection)
        member_records = [(member, existing_records.get(member.id)) for member in members]

    return render(request, 'accounting/collection/collection_update.html', {
        'form': form,
        'collection': collection,
        'member_records': member_records,
    })

# ===============================
# 徴収項目の削除（確認 → 実行）
# ===============================
@login_required
def collection_delete(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    if request.method == 'POST':
        year = collection.deadline.year
        collection.delete()
        return redirect('accounting:collection_list', year=year)

    return render(request, 'accounting/collection/collection_delete.html', {
        'collection': collection
    })