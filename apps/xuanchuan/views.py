from datetime import datetime
import json
import re

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.core import serializers
from pure_pagination import PageNotAnInteger, Paginator

from .models import MessageDraft, ObjMedia, Category
from users.models import UserProfile, Office, Team


class MessageDraftView(View):
    """
    宣传管理信息起草
    """

    def get(self, request):
        add_time = datetime.now()

        all_category = Category.objects.all()
        all_media = ObjMedia.objects.all()
        all_office = Office.objects.all()

        return render(request, 'xc_draft.html', {
            "add_time": add_time,
            "all_category": all_category,
            "all_media": all_media,
            "all_office": all_office,

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
            accept_users = request.POST.getlist('accept_user[]', [])

            message_draft = MessageDraft()
            message_draft.draft_user = request.user
            message_draft.title = title
            message_draft.status = status
            message_draft.add_time = time
            message_draft.start_time = start_time
            message_draft.end_time = end_time
            message_draft.content = content
            message_draft.remark = remark

            message_draft.save()

            lis = MessageDraft.objects.get(id=message_draft.id)
            # 保存类型
            for c in style:
                category = Category.objects.get(name=c)
                lis.category.add(category)
            # # 保存媒体对象
            for m in media:
                media = ObjMedia.objects.get(name=m)
                lis.media.add(media)

            # 修改   保存接受人的id
            for a in accept_users:
                accept_user = UserProfile.objects.get(id=a)
                if accept_user:
                    lis.accept_user.add(accept_user)

            recall = {"status": "success", "lis_id": message_draft.id}

            return HttpResponse(json.dumps(recall))

        return HttpResponse('{"status": "fail"}', content_type="application/json")


class GetReceiverView(View):
    """
    获取 小组下的成员
    """

    def get(self, request):
        team_id = request.GET.get('id', '')
        team = Team.objects.get(id=team_id)
        if team:
            data = serializers.serialize("json", team.userprofile_set.all(), fields=['pk', 'name'])

            return HttpResponse(data)


class MessageDraftFileUploadView(View):

    """
    保存宣传信息起草表附件
    """

    def post(self, request, *args, **kwargs):

        lis_id = request.POST.get('lis_id', '')
        file = request.FILES.get("file", None)

        if file:
            message_draft = MessageDraft.objects.get(id=lis_id)
            message_draft.file = file
            message_draft.save()

            return HttpResponse('{"status": "success"}', content_type="application/json")

        return HttpResponse('{"status": "fail"}', content_type="application/json")


class MessageInfoView(View):
    """
    宣传信息统计页面
    """
    def get(self, request):

        return render(request, 'information_count.html', {

        })


class MessageManagementView(View):
    """
    宣传信息管理页面
    """
    def get(self, request):
        return render(request, 'Publicity_management.html', {

        })


class MessageSearchView(View):
    """
    宣传信息查询页面
    """
    def get(self, request):
        all_messages = MessageDraft.objects.all()
        all_category = Category.objects.all()
        count = all_messages.count()
        count = count % 3 + 1

        title = request.GET.get("title", '')
        proposer = request.GET.get("proposer", '')
        category = request.GET.get("category", '')
        style = request.GET.get("style", '')

        if title:
            all_messages = all_messages.filter(title=title)
        if proposer:
            all_messages = all_messages.filter(draft_user__username=proposer)
        if category:
            all_messages = all_messages.filter(category__name=category)
        if style:
            all_messages = all_messages.filter(status=style)

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_messages, 3, request=request)

        messages = p.page(page)

        return render(request, 'Publish_query.html', {
            "all_messages": messages,
            "count": int(count),
            "all_category": all_category,
        })


class MessageCategoryManageView(View):
    """
    宣传信息类别管理页面
    """
    def get(self, request):

        all_category = Category.objects.all()

        return render(request, 'Category_management.html', {
            "all_category": all_category,
        })


class ItemsMakeCountView(View):

    """
    宣传物资制作统计页面
    """

    def get(self, request):

        return render(request, 'promo_count.html', {

        })


class ItemReceiverCountView(View):

    """
    宣传物资领用统计页面
    """

    def get(self, request):

        return render(request, 'receive_count.html', {

        })