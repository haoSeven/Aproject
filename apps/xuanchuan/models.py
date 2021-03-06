from datetime import datetime

from django.db import models

from users.models import UserProfile


class DraftBase(models.Model):
    draft_user = models.ForeignKey(UserProfile, verbose_name='起草人', related_name='draft_user')
    title = models.CharField(max_length=30, verbose_name='标题')
    status = models.CharField(choices=(('wait', '待审批'), ('success', '已审批')), max_length=10, verbose_name='状态'
                              , default='wait')
    style = models.CharField(max_length=20, default="", verbose_name="表单申请类型")

    add_time = models.DateTimeField(default='', verbose_name='申请时间')
    accept_user = models.ManyToManyField(UserProfile, verbose_name='接受人', related_name='accept_user')

    class Meta:
        verbose_name = '基础表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=20, verbose_name='类别名称')
    status = models.CharField(choices=(("stop", "停用"), ("active", "启用")), max_length=6,
                              verbose_name='状态', default='active')
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
    main = models.OneToOneField(DraftBase, verbose_name='基础信息')
    start_time = models.CharField(default='', verbose_name='开始时间', max_length=20)
    end_time = models.CharField(default='', verbose_name='结束时间', max_length=20)
    content = models.TextField(max_length=500, verbose_name='内容')
    remark = models.CharField(max_length=200, verbose_name='备注')
    file = models.FileField(upload_to='xc/files/%Y/%m', verbose_name='附件', max_length=100,
                            null=True, blank=True, default='')
    category = models.ManyToManyField(Category, verbose_name='类型')
    media = models.ManyToManyField(ObjMedia, verbose_name='媒体对象')
    opinion = models.ForeignKey(Opinion, verbose_name='领导意见', null=True, blank=True, default='')

    class Meta:
        verbose_name = '宣传信息起草表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.main.title

    def get_category(self):
        return self.category.all().count()

    def get_media(self):
        return self.media.all().count()
# end 宣传事务信息起草


class ItemsMake(models.Model):
    main = models.OneToOneField(DraftBase, verbose_name='基础信息')
    remark = models.CharField(max_length=200, verbose_name='备注')
    file = models.FileField(upload_to='xc/files/%Y/%m', verbose_name='附件', max_length=100,
                            null=True, blank=True, default='')
    opinion = models.ForeignKey(Opinion, verbose_name='领导意见', default='', null=True, blank=True)
    sum_cost = models.FloatField(verbose_name='总费用')

    class Meta:
        verbose_name = '宣传资料制作'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.style


class ItemMake(models.Model):
    name = models.CharField(max_length=20, verbose_name='宣传品名称', null=True, blank=True)
    require_time = models.CharField(default='', verbose_name='要求完成时间', max_length=20 )
    standard = models.CharField(max_length=20, verbose_name='规格', null=True, blank=True)
    nums = models.IntegerField(verbose_name='数量')
    unit = models.CharField(max_length=20, verbose_name='单位', null=True, blank=True)
    adv_com_name = models.CharField(max_length=30, verbose_name='广告公司名称')
    adv_com_contact = models.CharField(max_length=20, verbose_name='广告公司联系人', null=True, blank=True)
    adv_com_mobile = models.CharField(max_length=11, verbose_name='广告公司联系方式')
    cost = models.FloatField(verbose_name='费用')
    lis = models.ForeignKey(ItemsMake, verbose_name='宣传资料制作表')
    make_method = models.CharField(max_length=20, verbose_name='制作方式')
    category = models.CharField(max_length=20, default='', verbose_name='宣传品类别')

    class Meta:
        verbose_name = '宣传资料内容'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ItemsReceive(models.Model):
    main = models.OneToOneField(DraftBase, verbose_name='基础信息')
    remark = models.CharField(max_length=200, verbose_name='备注')
    file = models.FileField(upload_to='xc/files/%Y/%m', verbose_name='附件', max_length=100,
                            null=True, blank=True, default='')
    opinion = models.ForeignKey(Opinion, verbose_name='领导意见', default='', null=True, blank=True)

    class Meta:
        verbose_name = '宣传资料制作'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.main.title


class NeedItem(models.Model):
    name = models.CharField(max_length=20, verbose_name='宣传品名称', default='')
    unit = models.CharField(max_length=20, verbose_name='单位', default='')
    nums = models.IntegerField(verbose_name='数量', default=0)
    remark = models.CharField(max_length=50, verbose_name='备注', null=True, blank=True)
    use_method = models.CharField(max_length=20, verbose_name='使用方向', null=True, blank=True)
    lis = models.ForeignKey(ItemsReceive, verbose_name='宣传资料领用表')

    class Meta:
        verbose_name = '需要领用的宣传资料'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CategoryCount(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户', default='')
    tv_count = models.IntegerField(verbose_name='电视媒体类', default=0)
    internet_count = models.IntegerField(verbose_name='网络媒体类', default=0)
    lift_count = models.IntegerField(verbose_name='电梯海报类', default=0)
    news_count = models.IntegerField(verbose_name='新闻媒体类', default=0)
    webo_count = models.IntegerField(verbose_name='微博微信类', default=0)
    other_count = models.IntegerField(verbose_name='其他', default=0)

    class Meta:
        verbose_name = '宣传信息发布统计'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.name

    def get_sum(self):
        return self.tv_count + self.internet_count + self.lift_count + \
               self.news_count + self.webo_count + self.other_count


class ItemMakeCount(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户', default='')
    manual_count = models.IntegerField(verbose_name='手册', default=0)
    adv_count = models.IntegerField(verbose_name='广告', default=0)
    video_count = models.IntegerField(verbose_name='视频', default=0)
    leaflet_count = models.IntegerField(verbose_name='单张', default=0)
    other_count = models.IntegerField(verbose_name='其他', default=0)

    class Meta:
        verbose_name = '宣传物资领用统计'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.name

    def get_sum(self):
        return self.manual_count + self.adv_count + self.video_count + self.leaflet_count + self.other_count


class ItemReceiveCount(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户', default='')
    manual_count = models.IntegerField(verbose_name='手册', default=0)
    badge_count = models.IntegerField(verbose_name='胸章', default=0)
    pendant_count = models.IntegerField(verbose_name='吊坠', default=0)
    ticket_count = models.IntegerField(verbose_name='电影票', default=0)
    other_count = models.IntegerField(verbose_name='其他', default=0)

    class Meta:
        verbose_name = '宣传物资领用统计'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.name

    def get_sum(self):

        return self.manual_count + self.badge_count + self.pendant_count + self.ticket_count + self.other_count
