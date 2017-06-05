from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .forms import MessageDraftForm
from .models import MessageDraft


class MessageDraftView(View):
    """
    宣传管理信息起草
    """

    def get(self, request):
        message = MessageDraft()
        add_time = message.add_time


        return render(request, '', {
            "add_time": add_time,
        })

    def post(self, request):
        message = MessageDraft()
        message.draft_user = request.user
        message.add_time = request.POST.get('', '')
        message.title = request.POST.get('', '')
        message.start_time = request.POST.get('', '')
        pass
