# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-19 15:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('xuanchuan', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemsreceive',
            name='opinion',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='xuanchuan.Opinion', verbose_name='领导意见'),
        ),
    ]
