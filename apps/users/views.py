from django.shortcuts import render
from django.views.generic import View

from xuanchuan.models import MessageDraft



class Index(View):

    def get(self, request):
        all_messagedaft = MessageDraft.objects.filter(accept_user=request.user.id)

        return render(request, 'mywork.html', {
            'all_messagedaft': all_messagedaft,
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