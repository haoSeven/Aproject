from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse

from xuanchuan.models import MessageDraft, Opinion


class Index(View):

    def get(self, request):

        all_messagedaft = MessageDraft.objects.filter(accept_user=request.user.id, status='未审核')
        has_message = MessageDraft.objects.filter(accept_user=request.user.id, status='已审批')

        no_count = all_messagedaft.count()
        has_count = has_message.count()
        show = request.GET.get('shiwu' '')
        status = 1
        if show == 'daiban':
            status = 1
        elif show == 'yiban':
            status = 2

        return render(request, 'mywork.html', {
            'all_messagedaft': all_messagedaft,
            'has_message': has_message,
            "no_count": no_count,
            "has_count": has_count,
            'status': status,
        })


class HandleMessageDraftView(View):

    def get(self, request, message_id):
        messagedaft = MessageDraft.objects.get(id=message_id)
        categorys = messagedaft.category.all()
        medias = messagedaft.media.all()
        return render(request, 'sp_draft.html', {
            'messagedaft': messagedaft,
            "categorys": categorys,
            "medias": medias,
        })

    def post(self, request):
        content = request.POST.get('opinion', '')
        lis_id = request.POST.get('lis_id', '')

        opinion = Opinion()
        opinion.content = content
        opinion.leader = request.user
        opinion.save()

        lis = MessageDraft.objects.get(id=lis_id)
        if MessageDraft:
            lis.opinion_id = opinion.id
            lis.status = '已审批'
            lis.save()

            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "fail"})