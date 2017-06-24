# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-24 02:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PropagatePlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_timestyle', models.CharField(default='', max_length=10, verbose_name='计划时间类别')),
                ('team', models.CharField(default='', max_length=10, verbose_name='小组名称')),
                ('plan_style', models.CharField(default='', max_length=10, verbose_name='计划类别')),
                ('blame_person', models.CharField(max_length=10, verbose_name='负责人')),
                ('member', models.CharField(default='', max_length=10, verbose_name='成员')),
                ('start_time', models.CharField(default='', max_length=20, verbose_name='计划开始时间')),
                ('end_time', models.CharField(default='', max_length=20, verbose_name='计划结束时间')),
                ('content', models.TextField(default='', verbose_name='正文内容')),
                ('remark', models.CharField(max_length=200, verbose_name='备注')),
                ('file', models.FileField(blank=True, default='', null=True, upload_to='xc/files/%Y/%m', verbose_name='附件')),
            ],
            options={
                'verbose_name_plural': '宣传计划申请',
                'verbose_name': '宣传计划申请',
            },
        ),
        migrations.CreateModel(
            name='WorkTarget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_user', models.CharField(default='', max_length=10, verbose_name='负责人')),
                ('name', models.CharField(default='', max_length=20, verbose_name='项目名称')),
                ('content', models.CharField(default='', max_length=20, verbose_name='具体内容')),
                ('finish_time', models.CharField(default='', max_length=20, verbose_name='完成时间')),
                ('schedule', models.CharField(default='', max_length=10, verbose_name='进度')),
                ('complete_status', models.TextField(default='', verbose_name='完成情况')),
                ('is_finish', models.BooleanField(default=False, verbose_name='是否完成')),
                ('file', models.FileField(blank=True, default='', null=True, upload_to='xc/files/%Y/%m', verbose_name='附件')),
                ('propagate_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.PropagatePlan', verbose_name='计划表')),
            ],
        ),
    ]
