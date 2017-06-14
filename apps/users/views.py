from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse

from xuanchuan.models import MessageDraft, Opinion,DraftBase


class Index(View):

    def get(self, request):

        all_draft = DraftBase.objects.filter(accept_user=request.user.id, status='未审核').order_by('-add_time')
        has_draft = DraftBase.objects.filter(accept_user=request.user.id, status='已审批').order_by('-add_time')

        no_count = all_draft.count()
        has_count = has_draft.count()
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