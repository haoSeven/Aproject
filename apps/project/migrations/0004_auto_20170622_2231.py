# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-22 14:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_auto_20170622_2104'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scheme',
            options={'verbose_name': '宣传方案申请', 'verbose_name_plural': '宣传方案申请'},
        ),
        migrations.AlterField(
            model_name='scheme',
            name='main',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='xuanchuan.DraftBase', verbose_name='主表'),
        ),
    ]
