# _*_ coding:utf-8 _*_

from django.conf.urls import url

from .views import MessageDraftView, MessageInfoView, MessageManagementView, MessageSearchView, MessageDraftFileUploadView


__author__ = 'haoSev7'
__date__ = '2017/5/26 21:59'


urlpatterns = [
    # 宣传管理信息表
    url(r'^messagedraft/$', MessageDraftView.as_view(), name='message_draft'),

    url(r'^messageinfo/$', MessageInfoView.as_view(), name='message_info'),

    url(r'^management/$', MessageManagementView.as_view(), name='management'),

    url(r'^messagesearch/$', MessageSearchView.as_view(), name='messagesearch'),

    url(r'^messagedraftupload/$', MessageDraftFileUploadView.as_view(), name='message_upload')
]