# Generated by Django 5.1.1 on 2025-05-25 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice_management', '0003_alter_practiceattendance_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='practiceattendance',
            name='status',
            field=models.CharField(choices=[('present', '〇'), ('late', '△'), ('absent', '✕'), ('undecided', 'ー')], default='undecided', max_length=10),
        ),
        migrations.AlterField(
            model_name='practiceday',
            name='location',
            field=models.CharField(choices=[('地塩寮', '地塩寮'), ('２階共用室', '２階共用室'), ('地下共用室', '地下共用室'), ('4共20', '4共20'), ('4共21', '4共21'), ('4共30', '4共30'), ('BOX', 'BOX'), ('その他', 'その他'), ('-', '-')], default='-', max_length=100),
        ),
        migrations.AlterField(
            model_name='practiceday',
            name='status',
            field=models.CharField(choices=[('practice', '練習'), ('teacher_practice', '先生練習'), ('concert', '演奏会'), ('welcome', '新歓'), ('training_camp', '合宿'), ('none', 'なし')], default='none', max_length=20),
        ),
    ]
