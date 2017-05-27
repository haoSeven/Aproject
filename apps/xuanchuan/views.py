from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .forms import MessageDraftForm


class MessageView(View):
    """
    宣传管理信息发布
    """

    def get(self, request):
        return render(request, '', {})

    def post(self, request):
        message_draft_form = MessageDraftForm(request.POST)
        if message_draft_form.is_valid():
            message_draft_form.save()
            lis_id = message_draft_form.auto_id
            return HttpResponseRedirect(reverse('', args=[lis_id]))


class SendLeaderView(View):
    """
    发送给领导
    """
    def get(self, request, lis_id):
        return render(request, '', {})

    def post(self, request, lis_id):
        pass
