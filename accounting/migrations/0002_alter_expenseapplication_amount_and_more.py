# Generated by Django 5.1.1 on 2025-05-17 05:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0001_initial'),
        ('member', '0007_page_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenseapplication',
            name='amount',
            field=models.IntegerField(verbose_name='金額（円）'),
        ),
        migrations.AlterField(
            model_name='expenseapplication',
            name='applicant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='member.page'),
        ),
        migrations.AlterField(
            model_name='expenseapplication',
            name='status',
            field=models.CharField(choices=[('pending', '申請中'), ('refunded', '払い戻し済み'), ('rejected', '却下')], default='pending', max_length=10),
        ),
    ]
