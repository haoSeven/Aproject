# _*_ coding:utf-8 _*_

from django.conf.urls import url

from .views import MessageDraftView, MessageInfoView, MessageManagementView, MessageSearchView,\
    MessageDraftFileUploadView, MessageCategoryManageView


__author__ = 'haoSev7'
__date__ = '2017/5/26 21:59'


urlpatterns = [
    # 宣传管理信息申请表
    url(r'^messagedraft/$', MessageDraftView.as_view(), name='message_draft'),
    # 宣传信息统计页面
    url(r'^messageinfo/$', MessageInfoView.as_view(), name='message_info'),
    # 宣传信息管理页面
    url(r'^management/$', MessageManagementView.as_view(), name='management'),
    # 宣传信息查询页面
    url(r'^messagesearch/$', MessageSearchView.as_view(), name='messagesearch'),
    # 宣传信息申请表 附件上传
    url(r'^messagedraftupload/$', MessageDraftFileUploadView.as_view(), name='message_upload'),
    # 宣传信息类别管理页面
    url(r'^messagecategory/$', MessageCategoryManageView.as_view(), name='management_category'),
]