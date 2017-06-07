from django.db import models
from django.contrib.auth.models import AbstractUser


class Department(models.Model):
    name = models.CharField(max_length=20, verbose_name='部门名称')

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Office(models.Model):
    department = models.ForeignKey(Department, verbose_name='部门')
    office_name = models.CharField(max_length=20, verbose_name='科室名称')

    class Meta:
        verbose_name = '科室'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.office_name


class Team(models.Model):
    office = models.ForeignKey(Office, verbose_name='科室名称')
    team_name = models.CharField(max_length=20, verbose_name='小组名称')

    class Meta:
        verbose_name = '小组'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.team_name


class UserProfile(AbstractUser):
    """
    继承AbstractUser类
    自带email
    """
    name = models.CharField(max_length=12, verbose_name='姓名')
    gender = models.CharField(choices=(('male', '男'), ('female', '女')), max_length=6, verbose_name='性别')
    role = models.CharField(max_length=20, verbose_name='角色')
    position = models.CharField(max_length=20, verbose_name='职位')
    team = models.ForeignKey(Team, verbose_name='隶属小组', null=True, blank=True)
    mobile = models.CharField(max_length=11, verbose_name='电话', default='')

    def __str__(self):
        return self.username
