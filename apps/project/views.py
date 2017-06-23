import re
import json
from datetime import datetime

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

from xuanchuan.models import DraftBase
from .models import Scheme, AddScheme
from users.models import UserProfile, Office
# Create your views here.


class SchemeQueryView(View):

    """
    宣传方案查询
    """

    def get(self, request):
        all_scheme = Scheme.objects.all()
        # 计算页数
        count = all_scheme.count()
        count = count // 5 + 1

        return render(request, 'Scheme_query.html', {})


class SchemeDraftView(View):
    """
    宣传方案起草
    """

    def get(self, request):

        all_office = Office.objects.all()

        return render(request, 'xc_scheme.html', {
            "add_time": datetime.now(),
            "all_office": all_office,
        })

    def post(self, request):
        if request.is_ajax():
            title = request.POST.get('title', '')
            category = request.POST.get('category', '')
            principal = request.POST.get('principal', '')
            member = request.POST.get('member', '')
            budget = request.POST.get('budget', '')
            actual_cost = request.POST.get('actual_cost', '')
            start_time = request.POST.get('start_time', '')
            end_time = request.POST.get('end_time', '')
            remark = request.POST.get('remark', '')
            status = request.POST.get('status', '')
            content = request.POST.get('content', '')
            style = "宣传方案申请"
            accept_user = request.POST.getlist('accept_user[]', [])

            # 修改时间格式
            time = request.POST.get('add_time', '')
            patten = '年|月'
            time = re.sub(patten, '-', time)
            time = re.sub('日', '', time)

            if title:
                draft_base = DraftBase()
                draft_base.title = title
                draft_base.status = status
                draft_base.add_time = time
                draft_base.draft_user = request.user
                draft_base.style = style
                draft_base.save()

                scheme = Scheme()
                scheme.category = category
                scheme.principal = principal
                scheme.member = member
                scheme.budget = budget
                scheme.actual_cost = actual_cost
                scheme.start_time = start_time
                scheme.end_time = end_time
                scheme.remark = remark
                scheme.content = content
                scheme.main = draft_base
                scheme.save()

                lis_draft_base = DraftBase.objects.get(id=draft_base.id)
                for a in accept_user:
                    accept_user = UserProfile.objects.get(id=a)
                    if accept_user:
                        lis_draft_base.accept_user.add(accept_user)

                recall = {"status": "success", "lis_id": scheme.id}
                return HttpResponse(json.dumps(recall))

        return HttpResponse('{"status": "fail"}', content_type="application/json")


class AddSchemeDraftView(View):
    def post(self, request):
        lis_id = request.POST.get('lis_id', '')
        style_name = request.POST.get('style_name', '')
        content = request.POST.get('content', '')
        finish_time = request.POST.get('finish_time', '')
        target_user = request.POST.get('target_user', '')

        if lis_id and style_name:
            project_menu = AddScheme()
            project_menu.style_name = style_name
            project_menu.content = content
            project_menu.time = finish_time
            project_menu.principal = target_user
            project_menu.lis_id = lis_id
            project_menu.save()

            return HttpResponse('{"status": "success"}', content_type="application/json")
        return HttpResponse('{"status": "fail"}', content_type="application/json")

class SchemeFileUploadView(View):

    """
    保存宣传方案起草表附件
    """

    def post(self, request, *args, **kwargs):

        lis_id = request.POST.get('lis_id', '')
        file = request.FILES.get("file", None)

        if file:
            scheme = Scheme.objects.get(id=lis_id)
            scheme.file = file
            scheme.save()

            return HttpResponse('{"status": "success"}', content_type="application/json")

        return HttpResponse('{"status": "fail"}', content_type="application/json")
