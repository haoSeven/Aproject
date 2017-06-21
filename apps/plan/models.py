from datetime import datetime

from django.db import models

from users.models import UserProfile,Office
from xuanchuan.models import Opinion,DraftBase


class PropagatePlan(models.Model):
    main = models.OneToOneField(DraftBase, verbose_name='基础信息')
    plan_timestyle = models.CharField(max_length=10, verbose_name='计划时间类别', default='')
    team = models.CharField(max_length=10 , default='', verbose_name='小组名称')
    plan_style = models.CharField(max_length=10 , default='', verbose_name='计划类别')
    blame_person = models.CharField(max_length=10, verbose_name='负责人')
    member = models.CharField(max_length=10 , default='', verbose_name='成员')
    start_time = models.CharField(default='', verbose_name='计划开始时间', max_length=20)
    end_time = models.CharField(default='', verbose_name='计划结束时间', max_length=20)
    content = models.TextField(default='', verbose_name='正文内容')
    remark = models.CharField(max_length=200, verbose_name='备注')
    file = models.FileField(upload_to='xc/files/%Y/%m', verbose_name='附件', max_length=100,
                            null=True, blank=True, default='')
    opinion = models.ForeignKey(Opinion, verbose_name='领导意见', null=True, blank=True, default='')

    class Meta:
        verbose_name = '宣传计划申请'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.main.title


class WorkTarget(models.Model):
    target_user = models.CharField(default='', verbose_name='负责人', max_length=10)
    name = models.CharField(default='', verbose_name='项目名称', max_length=20)
    content = models.CharField(default='', verbose_name='具体内容', max_length=20)
    finish_time = models.CharField(default='', verbose_name='完成时间', max_length=20)
    schedule = models.CharField(max_length=10, verbose_name='进度', default='')
    complete_status = models.TextField(default='', verbose_name='完成情况')
    is_finish = models.BooleanField(verbose_name='是否完成', default=False)
    file = models.FileField(upload_to='xc/files/%Y/%m', verbose_name='附件', max_length=100,
                            null=True, blank=True, default='')
    propagate_plan = models.ForeignKey(PropagatePlan , verbose_name='计划表')