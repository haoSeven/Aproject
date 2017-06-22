"""Aproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve

from users.views import Index, HandleMessageDraftView, LoginView, LogoutView,HandleItemsReceiveView,\
    HandlePlanDraftView, InputPlanView, InputPlanScheduleView, InputPlanFileUploadView, HandleSchemeDraftView,\
    InputSchemeView

from xuanchuan.views import GetReceiverView, OverViewView
from plan.views import PlanSearchView
from .settings import MEDIA_ROOT


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 登录
    url(r'^login/$', LoginView.as_view(), name='login'),
    # 登出
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    # 首页
    url(r'^$', Index.as_view(), name='index'),
    # 宣传信息URL配置
    url(r'^xc/', include('xuanchuan.urls', namespace='xc')),
    # 工作计划信息URL配置
    url(r'^jh/', include('plan.urls', namespace='jh')),
    # 工作方案URL配置
    url(r'^fa/', include('project.urls', namespace='fa')),
    # 审批宣传信息申请
    url(r'^messagedraft/(?P<draft_id>\d+)&(?P<style>.*)/$', HandleMessageDraftView.as_view(), name='handle_message_draft'),
    #审批物资领用申请
    url(r'^itemreceiver/(?P<draft_id>\d+)&(?P<style>.*)/$', HandleItemsReceiveView.as_view(), name='handle_itemreveiver_draft'),
    #审批宣传计划申请
    url(r'^plandraft/(?P<draft_id>\d+)&(?P<style>.*)/$', HandlePlanDraftView.as_view(),name='handle_plan_draft'),
    #审批宣传方案申请
    url(r'^schemedraft/(?P<draft_id>\d+)&(?P<style>.*)/$', HandleSchemeDraftView.as_view(), name='handle_scheme_draft'),
    #宣传计划填报
    url(r'^inputplan/(?P<draft_id>\d+)&(?P<style>.*)/$', InputPlanView.as_view(),name='input_plan'),
    #宣传方案填报
    url(r'^inputscheme/(?P<draft_id>\d+)&(?P<style>.*)/$', InputSchemeView.as_view(), name='input_scheme'),
    #填报计划进度
    url(r'^planschedule/(?P<plan_id>\d+)/$', InputPlanScheduleView.as_view(), name='plan_schedule'),
    # 提交宣传信息审批建议
    url(r'^sendopinion/$', HandleMessageDraftView.as_view(), name='send_opinion'),
    # 提交物资领用审批建议
    url(r'^itemreceiveropinion/$', HandleItemsReceiveView.as_view(), name='itemreceiver_opinion'),
    # 提交计划信息审批建议
    url(r'^plandraftopinion/$', HandlePlanDraftView.as_view(), name='plandraft_opinion'),
    # 提交宣传方案建议
    url(r'^schemedraftopinion/$', HandleSchemeDraftView.as_view(), name='schemedraft_opinion'),
    #填写项目进度
    url(r'^inputschedule/$', InputPlanScheduleView.as_view(), name='input_schedule'),
    #项目进度文件上传
    url(r'^schedulefileupload/$', InputPlanFileUploadView.as_view(), name='schedule_file_upload'),
    # 获取发送人
    url(r'^getreceiver/$', GetReceiverView.as_view(), name='get_receiver'),
    # 宣传概览
    url(r'^overview/$', OverViewView.as_view(), name='over_view'),

    # media图像地址 配置上传文件访问地址函数
    url(r'^media/(?P<path>.*)/$', serve, {"document_root": MEDIA_ROOT}),
]
