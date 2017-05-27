# _*_ coding:utf-8 _*_

from django.conf.urls import url

from .views import MessageView, SendLeaderView

__author__ = 'haoSev7'
__date__ = '2017/5/26 21:59'


urlpatterns = [
    # 宣传管理信息表
    url(r'^message_draft/$', MessageView.as_view(), name='message_draft'),

    url(r'^send_leader/(?P<lis_id>\d+)/$', SendLeaderView.as_view(), name='send_leader'),
]