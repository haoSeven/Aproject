# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-22 12:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xuanchuan', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemmake',
            name='category',
            field=models.CharField(default='', max_length=20, verbose_name='宣传品类别'),
        ),
    ]
