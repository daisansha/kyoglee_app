# Generated by Django 5.1.1 on 2025-06-10 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0010_remove_cashpage_budget_balance_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cashbudget',
            name='budget_balance',
        ),
    ]
