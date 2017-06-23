import json
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse

from django.core.urlresolvers import reverse
from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout

from project.models import AddScheme,Scheme
from plan.models import PropagatePlan,WorkTarget
from xuanchuan.models import MessageDraft, Opinion, DraftBase, ItemsReceive, NeedItem
from .forms import LoginForm


class Index(View):

    def get(self, request):

        if request.user.is_authenticated():
            all_draft = DraftBase.objects.filter(accept_user=request.user, status='未审核').order_by('-add_time')
            has_draft = DraftBase.objects.filter(accept_user=request.user, status='已审批').order_by('-add_time')
            allplan_draft = DraftBase.objects.filter(draft_user=request.user, status='已审批', style='宣传计划申请').order_by('-add_time')
            allproject_draft = DraftBase.objects.filter(draft_user=request.user, status='已审批', style='宣传方案申请').order_by('-add_time')

            no_count = all_draft.count()
            has_count = has_draft.count()
            plan_count = allplan_draft.count()
            project_count = allproject_draft.count()
        else:
            all_draft = None
            has_draft = None
            allplan_draft = None
            allproject_draft = None
            no_count = 0
            has_count = 0
            plan_count = 0
            project_count = 0
        shiwu = request.GET.get('shiwu' '')
        style = request.GET.get('style' '')
        if shiwu == None:
            shiwu = 'daiban'
        if style == None:
            style = 'plan'

        return render(request, 'mywork.html', {
            'all_draft': all_draft,
            'has_draft': has_draft,
            "no_count": no_count,
            "has_count": has_count,
            "plan_count": plan_count,
            "project_count": project_count,
            'shiwu': shiwu,
            'style': style,
            'allplan_draft': allplan_draft,
            'allproject_draft': allproject_draft,
        })


class HandleMessageDraftView(View):

    def get(self, request, draft_id, style):
        draft = DraftBase.objects.get(id=draft_id, style=style)

        categorys = draft.messagedraft.category.all()
        medias = draft.messagedraft.media.all()
        return render(request, 'sp_draft.html', {
            'draft': draft,
            'categorys': categorys,
            'medias': medias,
        })

    def post(self, request):
        content = request.POST.get('opinion', '')
        lis_id = request.POST.get('lis_id', '')

        opinion = Opinion()
        opinion.content = content
        opinion.leader = request.user
        opinion.save()

        draft = DraftBase.objects.get(id=lis_id)

        if MessageDraft:
            draft.messagedraft.opinion_id = opinion.id
            draft.status = '已审批'
            draft.messagedraft.save()
            draft.save()

            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "fail"})

class HandleItemsReceiveView(View):

    def get(self, request, draft_id, style):

        draft = DraftBase.objects.get(id=draft_id, style=style)
        needitems = draft.itemsreceive.needitem_set.all()

        return render(request, 'sp_wzly.html', {
            'draft': draft,
            'needitems': needitems
        })

    def post(self, request):
        content = request.POST.get('opinion', '')
        lis_id = request.POST.get('lis_id', '')

        opinion = Opinion()
        opinion.content = content
        opinion.leader = request.user
        opinion.save()

        draft = DraftBase.objects.get(id=lis_id)

        if ItemsReceive:
            draft.itemsreceive.opinion_id = opinion.id
            draft.status = '已审批'
            draft.itemsreceive.save()
            draft.save()

            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "fail"})

class HandleItemMakeView(View):
    def get(self, request, draft_id, style):

        draft = DraftBase.objects.get(id=draft_id, style=style)
        items = draft.itemsmake.itemmake_set.all()

        return render(request, 'sp_itemmake.html', {
            'draft': draft,
            'items': items
        })
    def post(self, request):
        content = request.POST.get('opinion', '')
        lis_id = request.POST.get('lis_id', '')

        opinion = Opinion()
        opinion.content = content
        opinion.leader = request.user
        opinion.save()

        draft = DraftBase.objects.get(id=lis_id)

        if draft:
            draft.itemsmake.opinion_id = opinion.id
            draft.status = '已审批'
            draft.itemsmake.save()
            draft.save()

            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "fail"})

class HandlePlanDraftView(View):
    """
    审批计划页面
    """
    def get(self, request, draft_id, style):

        draft = DraftBase.objects.get(id=draft_id, style=style)
        project_menu = draft.propagateplan.worktarget_set.all()

        return render(request, 'sp_plan.html', {
            'draft': draft,
            'project_menu': project_menu
        })

    def post(self, request):
        content = request.POST.get('opinion', '')
        lis_id = request.POST.get('lis_id', '')

        opinion = Opinion()
        opinion.content = content
        opinion.leader = request.user
        opinion.save()

        draft = DraftBase.objects.filter(id=lis_id)
        if draft:
            draft = DraftBase.objects.get(id=lis_id)
            draft.propagateplan.opinion_id = opinion.id
            draft.status = '已审批'
            draft.propagateplan.save()
            draft.save()

            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "fail"})

class HandleSchemeDraftView(View):
    """
    审批方案页面
    """
    def get(self, request, draft_id, style):

        draft = DraftBase.objects.get(id=draft_id, style=style)
        scheme_messages = draft.scheme.addscheme_set.all()

        return render(request, 'sp_scheme.html', {
            'draft': draft,
            'scheme_messages': scheme_messages
        })

    def post(self, request):
        content = request.POST.get('opinion', '')
        lis_id = request.POST.get('lis_id', '')

        opinion = Opinion()
        opinion.content = content
        opinion.leader = request.user
        opinion.save()

        draft = DraftBase.objects.filter(id=lis_id)
        if draft:
            draft = DraftBase.objects.get(id=lis_id)
            draft.scheme.opinion_id= opinion.id
            draft.status = '已审批'
            draft.scheme.save()
            draft.save()

            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "fail"})

class InputPlanView(View):
    """
    获取填写计划页面
    """
    def get(self, request, draft_id, style):
        draft = DraftBase.objects.get(id=draft_id, style=style)
        project_menu = draft.propagateplan.worktarget_set.all()

        return render(request, 'tb_plan.html', {
            'draft': draft,
            'project_menu': project_menu
        })
class InputSchemeView(View):
    """
    获取填写方案页面
    """
    def get(self, request, draft_id, style):
        draft = DraftBase.objects.get(id=draft_id, style=style)
        scheme_messages = draft.scheme.addscheme_set.all()

        return render(request, 'tb_scheme.html', {
            'draft': draft,
            'scheme_messages': scheme_messages
        })

class InputPlanScheduleView(View):
    """
    填写计划进度
    """

    def get(self,request,plan_id):
        plan = WorkTarget.objects.get(id = plan_id)
        return render(request, 'Completion_table.html', {
            'plan': plan
        })

    def post(self,request):
        schedule = request.POST.get('schedule', '')
        complete_status = request.POST.get('complete_status', '')
        is_finish = request.POST.get('is_finish', '')
        lis_id = request.POST.get('lis_id', '')

        plan = WorkTarget.objects.filter(id=lis_id)
        if plan:
            plan = WorkTarget.objects.get(id=lis_id)
            plan.schedule = schedule
            plan.complete_status = complete_status
            plan.is_finish = is_finish
            plan.save()

            recall = {"status": "success"}
            return HttpResponse(json.dumps(recall))
        return JsonResponse({"status": "fail"})


class InputSchemeScheduleView(View):
    """
    填写方案进度
     """
    def get(self, request, scheme_id):
        addscheme = AddScheme.objects.get(id=scheme_id)

        return render(request, 'scheme_table.html', {
            'addscheme': addscheme
        })


    def post(self,request):
        schedule = request.POST.get('schedule', '')
        complete_status = request.POST.get('complete_status', '')
        is_finish = request.POST.get('is_finish', '')
        lis_id = request.POST.get('lis_id', '')

        scheme = AddScheme.objects.filter(id=lis_id)
        if scheme:
            scheme = AddScheme.objects.get(id=lis_id)
            scheme.schedule = schedule
            scheme.complete_status = complete_status
            scheme.is_finished = is_finish
            scheme.save()

            recall = {"status": "success"}
            return HttpResponse(json.dumps(recall))
        return JsonResponse({"status": "fail"})

class InputPlanFileUploadView(View):
    def post(self, request, *args, **kwargs):

        lis_id = request.POST.get('lis_id', '')
        file = request.FILES.get("file", None)

        if file:
            input_plan = WorkTarget.objects.get(id=lis_id)
            input_plan.file = file
            input_plan.save()
            return HttpResponse('{"status": "success"}', content_type="application/json")

        return HttpResponse('{"status": "fail"}', content_type="application/json")




class LoginView(View):
    """
    登录页面
    """
    def get(self, request):

        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {"msg": "用户未激活"})
            else:
                return render(request, 'login.html', {"msg": "用户名或密码错误"})
        else:
            return render(request, 'login.html', {"login_form": login_form})


class LogoutView(View):
    """
    登出
    """
    def get(self, request):
        if request.user.is_authenticated():
            logout(request)
            return HttpResponseRedirect(reverse('index'))