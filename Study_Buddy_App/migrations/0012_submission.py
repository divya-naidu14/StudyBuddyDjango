# Generated by Django 3.1.7 on 2024-03-31 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Study_Buddy_App', '0011_delete_day'),
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('task_name', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Study_Buddy_App.subject')),
            ],
        ),
    ]
