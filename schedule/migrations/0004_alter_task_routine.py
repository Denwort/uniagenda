# Generated by Django 5.0.3 on 2024-08-22 12:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_alter_routine_type_alter_routineday_routine_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='routine',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='schedule.routine'),
        ),
    ]
