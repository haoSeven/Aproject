from datetime import datetime
import re

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from .models import MessageDraft, ObjMedia, Category
from users.models import UserProfile


class MessageDraftView(View):
    """
    宣传管理信息起草
    """

    def get(self, request):
        add_time = datetime.now()

        return render(request, 'xc_draft.html', {
            "add_time": add_time,
        })


    def post(self, request):

        if request.is_ajax():

            title = request.POST.get('title', '')
            status = request.POST.get('state', '')

            # 修改时间格式
            time = request.POST.get('time', '')
            patten = '年|月'
            time = re.sub(patten, '-', time)
            time = re.sub('日', '', time)

            start_time = request.POST.get('start_time', '')
            end_time = request.POST.get('end_time', '')
            content = request.POST.get('content', '')
            remark = request.POST.get('remark', '')
            style = request.POST.getlist('style[]', [])
            media = request.POST.getlist('media[]', [])
            accept_user = request.POST.getlist('accept_user[]', [])
            file = request.POST.get('file', '')

            message_draft = MessageDraft()
            message_draft.draft_user = request.user
            message_draft.title = title
            message_draft.status = status
            message_draft.add_time = time
            message_draft.start_time = start_time
            message_draft.end_time = end_time
            message_draft.content = content
            message_draft.remark = remark
            message_draft.file = file

            # 保存文件 ！

            # message_draft.save()

            # lis = MessageDraft.objects.get(id=message_draft.id)
            # 保存类型
            # for c in style:
            #     category = Category(name=c)
            #     if not category:
            #         category.name = c
            #         category.save()
            #         lis.category.add(category)
            # # 保存媒体对象
            # for m in media:
            #     media = ObjMedia(name=m)
            #     if not media:
            #         media.name = m
            #         media.save()
            #         lis.media.add(media)
            #
            # # 修改   保存接受人的id
            # for a in accept_user:
            #     accept_user = UserProfile(id=a)
            #     if accept_user:
            #        lis.accept_user.add(accept_user)

            return HttpResponse('{"status": "success"}', content_type="application/json")

        return HttpResponse('{"status": "fail"}', content_type="application/json")

