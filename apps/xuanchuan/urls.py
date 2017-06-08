# _*_ coding:utf-8 _*_

from django.conf.urls import url

from .views import MessageDraftView


__author__ = 'haoSev7'
__date__ = '2017/5/26 21:59'


urlpatterns = [
    # 宣传管理信息表
    url(r'^messagedraft/$', MessageDraftView.as_view(), name='message_draft')
]