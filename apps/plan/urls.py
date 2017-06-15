from django.conf.urls import url

from .views import PlanSearchView

urlpatterns = [
    # 工作计划查询
    url(r'^plansearch/$', PlanSearchView.as_view(), name='plan_search'),
]