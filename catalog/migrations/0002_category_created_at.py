# Generated by Django 4.2.3 on 2023-07-28 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='created_at',
            field=models.DateField(auto_now=True, verbose_name='Дата создания'),
        ),
    ]
