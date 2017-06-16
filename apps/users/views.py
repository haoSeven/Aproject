from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout

from xuanchuan.models import MessageDraft, Opinion, DraftBase
from .forms import LoginForm


class Index(View):

    def get(self, request):

        if request.user.is_authenticated():
            all_draft = DraftBase.objects.filter(accept_user=request.user, status='未审核').order_by('-add_time')
            has_draft = DraftBase.objects.filter(accept_user=request.user, status='已审批').order_by('-add_time')

            no_count = all_draft.count()
            has_count = has_draft.count()
        else:
            all_draft = None
            has_draft = None
            no_count = 0
            has_count = 0
        show = request.GET.get('shiwu' '')
        status = 1
        if show == 'daiban':
            status = 1
        elif show == 'yiban':
            status = 2

        return render(request, 'mywork.html', {
            'all_draft': all_draft,
            'has_draft': has_draft,
            "no_count": no_count,
            "has_count": has_count,
            'status': status,
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