from django.conf.urls import url

from .views import SchemeQueryView, SchemeDraftView,SchemeFileUploadView,AddSchemeDraftView


urlpatterns = [
    # 宣传方案查询
    url(r'^Scheme_query/$', SchemeQueryView.as_view(), name='Scheme_query'),
    # 宣传方案起草
    url(r'^schemedraft/$', SchemeDraftView.as_view(), name='scheme_draft'),
    # 宣传方案详细信息
    url(r'^schememessage/$', AddSchemeDraftView.as_view(), name='scheme_message'),
    # 宣传方案附件上传
    url(r'^schemefileupload/$', SchemeFileUploadView.as_view(), name='scheme_file_upload'),
]
