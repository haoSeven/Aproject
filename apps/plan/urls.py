from django.conf.urls import url

from .views import PlanSearchView,NewPlanDraftView,AddNewPlanDraftView,NewPlanFileUploadView

urlpatterns = [
    # 工作计划查询
    url(r'^plansearch/$', PlanSearchView.as_view(), name='plan_search'),
   #新建宣传计划
    url(r'^plandraft/$', NewPlanDraftView.as_view(), name='plan_draft'),
    #详细项目计划
    url(r'^projectmenu/$', AddNewPlanDraftView.as_view(), name='project_menu'),
    #计划文件上传
    url(r'^planfileupload/$', NewPlanFileUploadView.as_view(), name='plan_file_upload'),
]