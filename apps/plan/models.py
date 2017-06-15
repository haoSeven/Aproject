from datetime import datetime

from django.db import models

from users.models import UserProfile,Office
from xuanchuan.models import Opinion,DraftBase


class PropagatePlan(models.Model):
    main = models.OneToOneField(DraftBase, verbose_name='基础信息')
    plan_timestyle = models.CharField(max_length=10, verbose_name='计划时间类别', default='')
    blame_person = models.CharField(max_length=10, verbose_name='负责人')
    plan_time = models.CharField(default='', verbose_name='计划时间', max_length=20)
    remark = models.CharField(max_length=200, verbose_name='备注')
    office = models.ManyToManyField(Office, verbose_name='小组')
    file = models.FileField(upload_to='xc/files/%Y/%m', verbose_name='附件', max_length=100,
                            null=True, blank=True, default='')
    opinion = models.ForeignKey(Opinion, verbose_name='领导意见', null=True, blank=True, default='')

    class Meta:
        verbose_name = '宣传计划申请'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.main.title

class WorkTarget(models.Model):
    target_user = models.ForeignKey(UserProfile, verbose_name='填指标者', related_name='target_user')
    add_time = models.DateTimeField(default='', verbose_name='申请时间')
    work_target = models.CharField(max_length=200, verbose_name='工作指标')
    finish_time = models.CharField(default='', verbose_name='完成时间', max_length=20)
    finish_number = models.IntegerField(default='', verbose_name='完成次数')
    content = models.TextField(max_length=500, verbose_name='内容')
    file = models.FileField(upload_to='xc/files/%Y/%m', verbose_name='附件', max_length=100,
                            null=True, blank=True, default='')
    remark = models.CharField(max_length=200, verbose_name='备注')
    propagate_plan = models.ForeignKey(PropagatePlan , verbose_name='计划表')