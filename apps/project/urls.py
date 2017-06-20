from django.conf.urls import url

from .views import SchemeQueryView, SchemeDraftView


urlpatterns = [
    # 宣传方案查询
    url(r'^Scheme_query/$', SchemeQueryView.as_view(), name='Scheme_query'),
    # 宣传方案起草
    url(r'^schemedraft/$', SchemeDraftView.as_view(), name='scheme_draft'),
]
