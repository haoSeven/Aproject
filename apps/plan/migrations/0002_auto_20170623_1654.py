# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-23 08:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('xuanchuan', '0001_initial'),
        ('plan', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='propagateplan',
            name='main',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='xuanchuan.DraftBase', verbose_name='基础信息'),
        ),
        migrations.AddField(
            model_name='propagateplan',
            name='opinion',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='xuanchuan.Opinion', verbose_name='领导意见'),
        ),
    ]
