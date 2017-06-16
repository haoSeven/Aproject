from django.conf.urls import url

from .views import SchemeQueryView
urlpatterns = [
        url(r'^Scheme_query/$', SchemeQueryView.as_view(), name='Scheme_query'),
]
