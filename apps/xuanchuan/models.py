from datetime import datetime

from django.db import models

from users.models import UserProfile


class Category(models.Model):
    name = models.CharField(max_length=20, verbose_name='类别名称')

    class Meta:
        verbose_name = '类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ObjMedia(models.Model):
    name = models.CharField(max_length=20, verbose_name='媒体对象')
    category = models.ForeignKey(Category, verbose_name='类别')

    class Meta:
        verbose_name = '媒体对象'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class MessageDraft(models.Model):
    draft_user = models.ForeignKey(UserProfile, verbose_name='起草人', related_name='draft_user')
    title = models.CharField(max_length=30, verbose_name='标题')
    start_time = models.DateTimeField(default=datetime.now, verbose_name='开始时间')
    end_time = models.DateTimeField(default=datetime.now, verbose_name='结束时间')
    content = models.TextField(max_length=500, verbose_name='内容')
    remark = models.CharField(max_length=200, verbose_name='备注')
    file = models.FileField(upload_to='xc/files/%Y/%m', verbose_name='附件', max_length=100,
                            null=True, blank=True, default='')
    media = models.ManyToManyField(ObjMedia, verbose_name='媒体对象')
    accept_user = models.ManyToManyField(UserProfile, verbose_name='接受人', related_name='accept_user')

    class Meta:
        verbose_name = '宣传信息起草表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Opinion(models.Model):
    content = models.CharField(max_length=200, verbose_name='意见')
    lis_id = models.IntegerField(verbose_name='表id', default='')
    lis_type = models.CharField(choices=((1, '宣传信息'), (2, '宣传品制作'), (3, '宣传物资领用'),
                                         (4, '工作计划'), (5, '工作方案')), max_length=10, default=1)
    leader = models.ForeignKey(UserProfile, verbose_name='领导', default='')

    class Meta:
        verbose_name = '意见'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.lis_type


class ItemDraft(models.Model):
    draft_user = models.ForeignKey(UserProfile, verbose_name='起草人')
    title = models.CharField(max_length=30, verbose_name='标题')
    remark = models.CharField(max_length=200, verbose_name='备注')
    file = models.FileField(upload_to='xc/files/%Y/%m', verbose_name='附件', max_length=100,
                            null=True, blank=True, default='')

    class Meta:
        verbose_name = '宣传资料制作'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class ItemCategory(models.Model):
    name = models.CharField(max_length=20, verbose_name='宣传品类别')

    class Meta:
        verbose_name = '宣传资料类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class MakeMethod(models.Model):
    name = models.CharField(max_length=20, verbose_name='制作方式')
    item_category = models.ForeignKey(ItemCategory, verbose_name='宣传品类别')

    class Meta:
        verbose_name = '制作方式'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=20, verbose_name='宣传品名称', null=True, blank=True)
    require_time = models.DateTimeField(default=datetime.now, verbose_name='要求完成时间')
    standard = models.CharField(max_length=20, verbose_name='规格', null=True, blank=True)
    nums = models.IntegerField(verbose_name='数量')
    unit = models.CharField(max_length=20, verbose_name='单位', null=True, blank=True)
    adv_com_name = models.CharField(max_length=30, verbose_name='广告公司名称')
    adv_com_contact = models.CharField(max_length=20, verbose_name='广告公司联系人', null=True, blank=True)
    adv_com_mobile = models.CharField(max_length=11, verbose_name='广告公司联系方式')
    cost = models.FloatField(verbose_name='费用')
    lis = models.ForeignKey(ItemDraft, verbose_name='宣传资料制作表')
    make_method = models.ForeignKey(MakeMethod, verbose_name='制作方式')

    class Meta:
        verbose_name = '宣传资料内容'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ItemReceive(models.Model):
    draft_user = models.ForeignKey(UserProfile, verbose_name='起草人')
    title = models.CharField(max_length=30, verbose_name='标题')
    remark = models.CharField(max_length=200, verbose_name='备注')
    file = models.FileField(upload_to='xc/files/%Y/%m', verbose_name='附件', max_length=100,
                            null=True, blank=True, default='')

    class Meta:
        verbose_name = '宣传资料制作'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class UseMethod(models.Model):
    name = models.CharField(max_length=15, verbose_name='使用方向')

    class Meta:
        verbose_name = '宣传资料使用方向'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class NeedItem(models.Model):
    name = models.CharField(max_length=20, verbose_name='宣传品名称', default='')
    unit = models.CharField(max_length=20, verbose_name='单位', default='')
    nums = models.IntegerField(verbose_name='数量', default=0)
    remark = models.CharField(max_length=50, verbose_name='备注', null=True, blank=True)
    use_method = models.ForeignKey(UseMethod, verbose_name='使用方向')
    lis = models.ForeignKey(ItemReceive, verbose_name='宣传资料领用表')

    class Meta:
        verbose_name = '需要领用的宣传资料'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name