from django.db import models

from xuanchuan.models import DraftBase, Opinion

# Create your models here.


class Scheme(models.Model):
    main = models.ForeignKey(DraftBase, verbose_name='主表')
    category = models.CharField(max_length=20, verbose_name='方案类别', default='')
    principal = models.CharField(max_length=20, verbose_name='负责人', default='')
    member = models.CharField(max_length=30, verbose_name='成员', default='')
    budget = models.FloatField(verbose_name='预算', default=0)
    actual_cost = models.FloatField(verbose_name='实际费用', default=0)
    start_time = models.CharField(max_length=20, verbose_name='方案开始时间', default='')
    end_time = models.CharField(max_length=20, verbose_name='方案结束时间', default='')
    content = models.TextField(verbose_name='内容', default='')
    remark = models.CharField(verbose_name='备注', max_length=100, default='')
    file = models.FileField(upload_to='xc/files/%Y/%m', verbose_name='附件', max_length=100,
                            null=True, blank=True, default='')
    opinion = models.ForeignKey(Opinion, verbose_name='领导意见', default='')


class AddScheme(models.Model):
    content = models.CharField(max_length=50, verbose_name='具体内容', default='')
    time = models.CharField(max_length=20, verbose_name='要求完成时间', default='')
    principal = models.CharField(max_length=10, verbose_name='负责人', default='')
    lis = models.ForeignKey(Scheme, verbose_name='方案表')
    schedule = models.CharField(max_length=10, verbose_name='进度', default='')
    is_finished = models.BooleanField(verbose_name='是否完成', default=False)
