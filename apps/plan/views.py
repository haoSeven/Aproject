from datetime import datetime


from django.shortcuts import render
from django.views.generic import View


from .models import PropagatePlan
from pure_pagination import PageNotAnInteger, Paginator
class PlanSearchView(View):

    def get(self, request):
        # 获取工作计划的所有申请表
        all_plan = PropagatePlan.objects.all()
        # 计算页数
        count = all_plan.count()
        count = count % 3 + 1

        title = request.GET.get("title", '')
        proposer = request.GET.get("proposer", '')
        timestyle = request.GET.get("timestyle", '')
        style = request.GET.get("style", '')

        if title:
            all_plan = all_plan.filter(main__title=title)
        if proposer:
            all_plan = all_plan.filter(main__draft_user__username=proposer)
        if timestyle:
            all_plan = all_plan.filter(plan_timestyle=timestyle)
        if style:
            all_plan = all_plan.filter(main__status=style)

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_plan, 3, request=request)

        messages = p.page(page)
        return render(request, 'workplan_search.html',{
            "all_plan": messages,
            "count": count
        })