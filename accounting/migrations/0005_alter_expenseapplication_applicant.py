# Generated by Django 5.1.1 on 2025-05-17 22:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0004_remove_expenseapplication_status_and_more'),
        ('member', '0012_remove_page_role_remove_page_user_member'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenseapplication',
            name='applicant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='member.member'),
        ),
    ]
