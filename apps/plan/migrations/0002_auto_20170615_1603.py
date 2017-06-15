# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-15 08:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('plan', '0001_initial'),
        ('users', '0001_initial'),
        ('xuanchuan', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='worktarget',
            name='target_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target_user', to=settings.AUTH_USER_MODEL, verbose_name='填指标者'),
        ),
        migrations.AddField(
            model_name='propagateplan',
            name='main',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='xuanchuan.DraftBase', verbose_name='基础信息'),
        ),
        migrations.AddField(
            model_name='propagateplan',
            name='office',
            field=models.ManyToManyField(to='users.Office', verbose_name='小组'),
        ),
        migrations.AddField(
            model_name='propagateplan',
            name='opinion',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='xuanchuan.Opinion', verbose_name='领导意见'),
        ),
    ]
