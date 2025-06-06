# accounting/views/collection_views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from accounting.models.collection_models import Collection, CollectionRecord
from accounting.forms.collection_forms import CollectionForm, CollectionRecordForm, CollectionRecordFormSet
from member.models import Member
from django.db import models

# 会計アプリのトップ
@login_required
def accounting_index(request):
    return render(request, 'accounting/index.html')

# 徴収作成
from django.forms import formset_factory

...

@login_required
def collection_create(request):
    members = Member.objects.all().order_by('name')

    if request.method == 'POST':
        form = CollectionForm(request.POST)
        record_forms = []
        for member in members:
            record_form = CollectionRecordForm(request.POST, prefix=str(member.id))
            record_form.instance.member = member  # ← 🔴 POST時に必要
            record_forms.append(record_form)

        if form.is_valid() and all(rf.is_valid() for rf in record_forms):
            collection = form.save()
            for record_form in record_forms:
                record = record_form.save(commit=False)
                record.collection = collection
                if record.status == "不要":
                    record.amount = 0
                record.save()
            return redirect('accounting:collection_list', year=collection.deadline.year)
    else:
        form = CollectionForm()
        record_forms = []
        for member in members:
            record_form = CollectionRecordForm(
                prefix=str(member.id),
                initial={'member': member, 'amount': 0, 'status': '未'}
            )
            record_form.instance.member = member  # ← 🔵 表示時も name 出すためにセット
            record_forms.append(record_form)

    return render(request, 'accounting/collection/collection_create.html', {
        'form': form,
        'record_forms': record_forms,
        'members': members,
    })



# 年ごとの徴収一覧
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

# 詳細（readonly）
@login_required
def collection_detail(request, year, pk):
    collection = get_object_or_404(Collection, pk=pk)
    form = CollectionForm(instance=collection)
    for field in form.fields.values():
        field.disabled = True

    formset = CollectionRecordFormSet(queryset=collection.records.all())
    for form in formset:
        for field in form.fields.values():
            field.disabled = True

    return render(request, 'accounting/collection/collection_detail.html', {
        'collection': collection,
        'form': form,
        'formset': formset,
    })

# 更新（財務のみステータス編集可能）
@login_required
def collection_update(request, pk):
    collection = get_object_or_404(Collection, pk=pk)

    if request.method == 'POST':
        form = CollectionForm(request.POST, instance=collection)
        formset = CollectionRecordFormSet(request.POST, queryset=collection.records.all())

        if form.is_valid() and formset.is_valid():
            form.save()
            for record_form in formset:
                record = record_form.save(commit=False)
                if record.status == "不要":
                    record.amount = 0
                record.save()
            return redirect('accounting:collection_detail', year=collection.deadline.year, pk=collection.pk)

    else:
        form = CollectionForm(instance=collection)
        records = collection.records.all().order_by(
            models.Case(
                models.When(status='未', then=0),
                models.When(status='済', then=1),
                models.When(status='不要', then=2),
                default=3,
                output_field=models.IntegerField()
            )
        )
        formset = CollectionRecordFormSet(queryset=records)

        # 財務以外は編集できないように制御
        if not request.user.member.is_financial:
            for f in form.fields.values():
                f.disabled = True
            for form_ in formset:
                for field in ['amount', 'status']:
                    form_.fields[field].disabled = True

    return render(request, 'accounting/collection/collection_update.html', {
        'collection': collection,
        'form': form,
        'formset': formset,
    })

# 削除
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
