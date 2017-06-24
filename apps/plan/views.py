from datetime import datetime
import json
import re

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from xuanchuan.models import DraftBase
from users.models import UserProfile, Office, Team
from .models import PropagatePlan,WorkTarget
from pure_pagination import PageNotAnInteger, Paginator


class NewPlanDraftView(View):
    """
    新建宣传计划
    """
    def get(self,request):
        add_time = datetime.now()
        all_office = Office.objects.all()

        return  render(request, 'xc_plan2.html', {
            'add_time': add_time,
            "all_office": all_office,
        })

    def post(self,request):
        if request.is_ajax():
            title = request.POST.get('title', '')
            status = request.POST.get('state', '')

            # 修改时间格式
            time = request.POST.get('apply_time', '')
            patten = '年|月'
            time = re.sub(patten, '-', time)
            time = re.sub('日', '', time)

            remark = request.POST.get('remark', '')
            accept_users = request.POST.getlist('accept_user[]', [])
            style = request.POST.get('style', '')
            start_time = request.POST.get('start_time', '')
            end_time = request.POST.get('end_time', '')
            blamer = request.POST.get('blamer', '')
            member = request.POST.get('member', '')
            plan_style = request.POST.get('plan_style', '')
            team_name = request.POST.get('team_name', '')
            time_style = request.POST.get('time_style', '')
            content = request.POST.get('content', '')

            draft_base = DraftBase()
            draft_base.draft_user = request.user
            draft_base.title = title
            draft_base.status = status
            draft_base.add_time = time
            draft_base.style = style
            draft_base.save()

            plan_draft = PropagatePlan()
            plan_draft.plan_timestyle = time_style
            plan_draft.team = team_name
            plan_draft.plan_style = plan_style
            plan_draft.blame_person = blamer
            plan_draft.member = member
            plan_draft.start_time = start_time
            plan_draft.end_time = end_time
            plan_draft.remark = remark
            plan_draft.content = content
            plan_draft.main = draft_base
            plan_draft.save()

            lis_draft_base = DraftBase.objects.get(id=draft_base.id)
            # 修改   保存接受人的id
            for a in accept_users:
                accept_user = UserProfile.objects.get(id=a)
                if accept_user:
                    lis_draft_base.accept_user.add(accept_user)

            recall = {"status": "success", "lis_id": plan_draft.id}

            return HttpResponse(json.dumps(recall))
        return HttpResponse('{"status": "fail"}', content_type="application/json")


class AddNewPlanDraftView(View):

    def post(self, request):
        lis_id = request.POST.get('lis_id', '')
        name = request.POST.get('name', '')
        content = request.POST.get('content', '')
        finish_time = request.POST.get('finish_time', '')
        target_user = request.POST.get('target_user', '')

        if lis_id and name:
            project_menu = WorkTarget()
            project_menu.name = name
            project_menu.content = content
            project_menu.finish_time = finish_time
            project_menu.target_user = target_user
            project_menu.propagate_plan_id = lis_id
            project_menu.save()

            return HttpResponse('{"status": "success"}', content_type="application/json")
        return HttpResponse('{"status": "fail"}', content_type="application/json")


class NewPlanFileUploadView(View):
    def post(self, request, *args, **kwargs):

        lis_id = request.POST.get('lis_id', '')
        file = request.FILES.get("file", None)

        if file:
            plan_draft = PropagatePlan.objects.get(id=lis_id)
            plan_draft.file = file
            plan_draft.save()

            return HttpResponse('{"status": "success"}', content_type="application/json")

        return HttpResponse('{"status": "fail"}', content_type="application/json")


class PlanSearchView(View):

    def get(self, request):
        # 获取工作计划的所有申请表
        all_plan = PropagatePlan.objects.all()
        # 计算页数
        count = all_plan.count()
        count = count // 5 + 1

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

        p = Paginator(all_plan, 5, request=request)

        messages = p.page(page)
        return render(request, 'workplan_search.html',{
            "all_plan": messages,
            "count": count
        })