from datetime import datetime

from django.db import models

from users.models import UserProfile


class Category(models.Model):
    name = models.CharField(max_length=20, verbose_name='类别名称')
    status = models.CharField(choices=(("ty", "停用"), ("qy", "启用")), max_length=5, verbose_name='状态', default='qy')
    create_user = models.ForeignKey(UserProfile, verbose_name='创建人', default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='申请时间')

    class Meta:
        verbose_name = '类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ObjMedia(models.Model):
    name = models.CharField(max_length=20, verbose_name='媒体对象')

    class Meta:
        verbose_name = '媒体对象'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Opinion(models.Model):
    content = models.CharField(max_length=100, verbose_name='意见')
    leader = models.ForeignKey(UserProfile, verbose_name='领导', default='')

    class Meta:
        verbose_name = '意见'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


class MessageDraft(models.Model):
    draft_user = models.ForeignKey(UserProfile, verbose_name='起草人', related_name='draft_user')
    title = models.CharField(max_length=30, verbose_name='标题')
    status = models.CharField(choices=(('wait', '待审批'), ('success', '已审批')), max_length=10, verbose_name='状态'
                              , default='wait')
    style = models.CharField(max_length=20, default="宣传信息申请", verbose_name="宣传信息申请")
    add_time = models.DateTimeField(default='', verbose_name='申请时间')
    start_time = models.CharField(default='', verbose_name='开始时间', max_length=20)
    end_time = models.CharField(default='', verbose_name='结束时间', max_length=20)
    content = models.TextField(max_length=500, verbose_name='内容')
    remark = models.CharField(max_length=200, verbose_name='备注')
    file = models.FileField(upload_to='xc/files/%Y/%m', verbose_name='附件', max_length=100,
                            null=True, blank=True, default='')
    category = models.ManyToManyField(Category, verbose_name='类型')
    media = models.ManyToManyField(ObjMedia, verbose_name='媒体对象')
    accept_user = models.ManyToManyField(UserProfile, verbose_name='接受人', related_name='message_accept_user')
    opinion = models.ForeignKey(Opinion, verbose_name='领导意见', null=True, blank=True, default='')

    class Meta:
        verbose_name = '宣传信息起草表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
# end 宣传事务信息起草


class Items(models.Model):
    draft_user = models.ForeignKey(UserProfile, verbose_name='起草人')
    title = models.CharField(max_length=30, verbose_name='标题')
    status = models.CharField(choices=(('wait', '待审批'), ('success', '已审批')), max_length=10, verbose_name='状态'
                              , default='wait')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    remark = models.CharField(max_length=200, verbose_name='备注')
    file = models.FileField(upload_to='xc/files/%Y/%m', verbose_name='附件', max_length=100,
                            null=True, blank=True, default='')
    accept_user = models.ManyToManyField(UserProfile, verbose_name='接受人', related_name='items_accept_user')
    opinion = models.ForeignKey(Opinion, verbose_name='领导意见')

    class Meta:
        verbose_name = '宣传资料制作'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class ItemMake(models.Model):
    name = models.CharField(max_length=20, verbose_name='宣传品名称', null=True, blank=True)
    require_time = models.DateTimeField(default=datetime.now, verbose_name='要求完成时间')
    standard = models.CharField(max_length=20, verbose_name='规格', null=True, blank=True)
    nums = models.IntegerField(verbose_name='数量')
    unit = models.CharField(max_length=20, verbose_name='单位', null=True, blank=True)
    adv_com_name = models.CharField(max_length=30, verbose_name='广告公司名称')
    adv_com_contact = models.CharField(max_length=20, verbose_name='广告公司联系人', null=True, blank=True)
    adv_com_mobile = models.CharField(max_length=11, verbose_name='广告公司联系方式')
    cost = models.FloatField(verbose_name='费用')
    lis = models.ForeignKey(Items, verbose_name='宣传资料制作表')
    make_method = models.CharField(max_length=20, verbose_name='制作方式')

    class Meta:
        verbose_name = '宣传资料内容'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


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
    lis = models.ForeignKey(Items, verbose_name='宣传资料领用表')

    class Meta:
        verbose_name = '需要领用的宣传资料'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name