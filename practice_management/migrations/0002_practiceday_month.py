# Generated by Django 5.1.1 on 2025-05-24 09:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='practiceday',
            name='month',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='days', to='practice_management.practicemonth'),
        ),
    ]
