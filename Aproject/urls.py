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

from users.views import Index, HandleMessageDraftView
from xuanchuan.views import GetReceiverView
from .settings import MEDIA_ROOT


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 首页
    url(r'^$', Index.as_view(), name='index'),
    # 宣传信息URL配置
    url(r'^xc/', include('xuanchuan.urls', namespace='xc')),
    # 审批宣传信息申请
    url(r'^messagedraft/(?P<draft_id>\d+)&(?P<style>.*)/$', HandleMessageDraftView.as_view(), name='handle_message_draft'),
    # 提交建议
    url(r'^sendopinion/$', HandleMessageDraftView.as_view(), name='send_opinion'),
    # 获取发送人
    url(r'^getreceiver/$', GetReceiverView.as_view(), name='get_receiver'),

    # media图像地址 配置上传文件访问地址函数
    url(r'^media/(?P<path>.*)/$', serve, {"document_root": MEDIA_ROOT}),
]
