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

from .models import MessageDraft, ObjMedia, Category, ItemsMake, ItemsReceive, DraftBase, CategoryCount,\
    ItemMakeCount, ItemReceiveCount, NeedItem, ItemMake
from plan.models import PropagatePlan
from project.models import Scheme
from users.models import UserProfile, Office, Team
from utils.mixin_utils import LoginRequiredMixin


class MessageDraftView(LoginRequiredMixin, View):
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
            category = request.POST.getlist('category[]', [])
            media = request.POST.getlist('media[]', [])
            accept_users = request.POST.getlist('accept_user[]', [])
            style = request.POST.get('style', '')

            draft_base = DraftBase()
            draft_base.draft_user = request.user
            draft_base.title = title
            draft_base.status = status
            draft_base.add_time = time
            draft_base.style = style
            draft_base.save()

            message_draft = MessageDraft()
            message_draft.start_time = start_time
            message_draft.end_time = end_time
            message_draft.content = content
            message_draft.remark = remark
            message_draft.main = draft_base
            message_draft.save()

            lis_message = MessageDraft.objects.get(id=message_draft.id)
            lis_draft_base = DraftBase.objects.get(id=draft_base.id)
            category_count = CategoryCount.objects.filter(user=request.user)

            # 保存类型
            for c in category:
                category = Category.objects.get(name=c)
                lis_message.category.add(category)
                if category_count:
                    category_count = CategoryCount.objects.get(user=request.user)
                    if c == '电视媒体':
                        category_count.tv_count += 1
                        category_count.save()
                    elif c == '网络媒体':
                        category_count.internet_count += 1
                        category_count.save()
                    elif c == '电梯海报':
                        category_count.lift_count += 1
                        category_count.save()
                    elif c == '新闻稿件':
                        category_count.news_count += 1
                        category_count.save()
                    elif c == '微博微信':
                        category_count.webo_count += 1
                        category_count.save()
                    else:
                        category_count.other_count += 1
                        category_count.save()
                else:
                    category_count = CategoryCount()
                    category_count.user = request.user
                    if c == '电视媒体':
                        category_count.tv_count += 1
                        category_count.save()
                    elif c == '网络媒体':
                        category_count.internet_count += 1
                        category_count.save()
                    elif c == '电梯海报':
                        category_count.lift_count += 1
                        category_count.save()
                    elif c == '新闻稿件':
                        category_count.news_count += 1
                        category_count.save()
                    elif c == '微博微信':
                        category_count.webo_count += 1
                        category_count.save()
                    else:
                        category_count.other_count += 1
                        category_count.save()

            # # 保存媒体对象
            for m in media:
                media = ObjMedia.objects.get(name=m)
                lis_message.media.add(media)

            # 修改   保存接受人的id
            for a in accept_users:
                accept_user = UserProfile.objects.get(id=a)
                if accept_user:
                    lis_draft_base.accept_user.add(accept_user)

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


class MessageInfoView(LoginRequiredMixin, View):
    """
    宣传信息统计页面
    """
    def get(self, request):

        category_count = CategoryCount.objects.all()
        tv_sum = 0
        inter_sum = 0
        lift_sum = 0
        news_sum = 0
        weibo_sum = 0
        other_sum = 0
        for c in category_count:
            tv_sum += c.tv_count
            inter_sum += c.internet_count
            lift_sum += c.lift_count
            news_sum += c.news_count
            weibo_sum += c.webo_count
            other_sum += c.other_count
        all_sum = tv_sum + inter_sum + lift_sum + news_sum + weibo_sum + other_sum

        return render(request, 'information_count.html', {
            "category_count": category_count,
            'tv_sum': tv_sum,
            'inter_sum': inter_sum,
            'lift_sum': lift_sum,
            'news_sum': news_sum,
            'weibo_sum': weibo_sum,
            'other_sum': other_sum,
            'all_sum': all_sum,
        })


class MessageManagementView(LoginRequiredMixin, View):
    """
    宣传信息管理页面
    """
    def get(self, request):
        return render(request, 'Publicity_management.html', {

        })


class MessageSearchView(LoginRequiredMixin, View):
    """
    宣传信息查询页面
    """
    def get(self, request):
        all_messages = MessageDraft.objects.all()
        all_category = Category.objects.all()
        count = all_messages.count()
        count = count // 3 + 1

        title = request.GET.get("title", '')
        proposer = request.GET.get("proposer", '')
        category = request.GET.get("category", '')
        status = request.GET.get("style", '')

        if title:
            all_messages = all_messages.filter(main__title=title)
        if proposer:
            all_messages = all_messages.filter(main__draft_user__name=proposer)
        if category:
            all_messages = all_messages.filter(category__name=category)
        if status:
            all_messages = all_messages.filter(main__status=status)

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


class MessageCategoryManageView(LoginRequiredMixin, View):
    """
    宣传信息类别管理页面
    """
    def get(self, request):

        all_category = Category.objects.filter()

        return render(request, 'Category_management.html', {
            "all_category": all_category,
        })


class ItemsMakeSearchView(LoginRequiredMixin, View):
    """
    宣传物资制作查询页面
    """
    def get(self, request):
        # 获取宣传物资制作的所有申请表
        all_itemsmakemessage = ItemsMake.objects.all()
        # 计算页数
        count = all_itemsmakemessage.count()
        count = count // 3 + 1
        # 获取前端传递的 查询条件
        title = request.GET.get("title", '')
        proposer = request.GET.get("proposer", '')
        makestyle = request.GET.get("makestyle", '')
        minsum = request.GET.get("minsum", 0)
        if minsum == '':
            minsum = 0
        else:
            minsum = int(minsum)

        maxsum = request.GET.get("maxsum", 0)
        if maxsum == '':
            maxsum = 0
        else:
            maxsum = int(maxsum)
        style = request.GET.get("style", '')

        # 对前端传递的查询条件进行过滤
        if title:
            all_itemsmakemessage = all_itemsmakemessage.filter(main__title=title)
        if proposer:
            all_itemsmakemessage = all_itemsmakemessage.filter(main__draft_user__username=proposer)
        if style:
            all_itemsmakemessage = all_itemsmakemessage.filter(main__status=style)

        if minsum and maxsum == 0:
            all_itemsmakemessage = all_itemsmakemessage.filter(sum_cost__gte=minsum)
        elif minsum == 0 and maxsum:
            all_itemsmakemessage = all_itemsmakemessage.filter(sum_cost__lte=maxsum)
        elif minsum and maxsum:
            all_itemsmakemessage = all_itemsmakemessage.filter(sum_cost__range=(minsum, maxsum))

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_itemsmakemessage, 3, request=request)

        messages = p.page(page)
        return render(request, 'item_make_search.html', {
            "all_itemsmakemessage": messages,
            "count": int(count)
        })


class ItemsMakeCountView(LoginRequiredMixin, View):

    """
    宣传物资制作统计页面
    """

    def get(self, request):

        all_item_make_count = ItemMakeCount.objects.all()

        manual_sum = 0
        adv_sum = 0
        video_sum = 0
        leaflet_sum = 0
        other_sum = 0

        for i in all_item_make_count:
            manual_sum += i.manual_count
            adv_sum += i.adv_count
            video_sum += i.video_count
            leaflet_sum += i.leaflet_count
            other_sum += i.other_count
        all_sum = manual_sum + adv_sum + video_sum + leaflet_sum + other_sum

        return render(request, 'promo_count.html', {
            "all_item_make_count": all_item_make_count,
            "manual_sum": manual_sum,
            "adv_sum": adv_sum,
            "video_sum": video_sum,
            "leaflet_sum": leaflet_sum,
            "other_sum": other_sum,
            "all_sum": all_sum
        })


class ItemReceiverSearchView(LoginRequiredMixin, View):

    """
    宣传物资领用查询页面
    """
    def get(self,request):
        all_itemreceivemessage = ItemsReceive.objects.all()
        count = all_itemreceivemessage.count()
        count = count // 3 + 1

        title = request.GET.get("title", '')
        proposer = request.GET.get("proposer", '')
        proposedepartment = request.GET.get("proposedepartment", '')
        style = request.GET.get("style", '')

        if title:
            all_itemreceivemessage = all_itemreceivemessage.filter(main__title=title)
        if proposer:
            all_itemreceivemessage = all_itemreceivemessage.filter(main__draft_user__username=proposer)
        if proposedepartment:
            all_itemreceivemessage = all_itemreceivemessage.filter(draft_user__team__team_name=proposedepartment)
        if style:
            all_itemreceivemessage = all_itemreceivemessage.filter(main__status=style)


        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_itemreceivemessage, 3, request=request)

        messages = p.page(page)

        return render(request, 'item_receive_search.html', {
            "all_itemreceivemessage": messages,
            "count": count
        })


class ItemReceiverCountView(LoginRequiredMixin, View):

    """
    宣传物资领用统计页面
    """

    def get(self, request):

        all_item_receive_count = ItemReceiveCount.objects.all()

        manual_sum = 0
        badge_sum = 0
        pendant_sum = 0
        ticket_sum = 0
        other_sum = 0

        for i in all_item_receive_count:
            manual_sum += i.manual_count
            badge_sum += i.badge_count
            pendant_sum += i.pendant_count
            ticket_sum += i.ticket_count
            other_sum += i.other_count
        all_sum = manual_sum + badge_sum + pendant_sum + ticket_sum + other_sum

        return render(request, 'receive_count.html', {
            "all_item_receive_count": all_item_receive_count,
            "manual_sum": manual_sum,
            "badge_sum": badge_sum,
            "pendant_sum": pendant_sum,
            "ticket_sum": ticket_sum,
            "other_sum": other_sum,
            "all_sum": all_sum,
        })


class ItemMakeView(LoginRequiredMixin, View):

    """
    宣传物资制作页面
    """

    def get(self, request):
        add_time = datetime.now()
        all_office = Office.objects.all()

        return render(request, 'item_make.html', {
            'add_time': add_time,
            "all_office": all_office,
        })

    def post(self, request):

        title = request.POST.get('title', '')
        status = request.POST.get('status', '')
        remark = request.POST.get('remark', '')
        accept_users = request.POST.getlist('accept_user[]', [])
        all_cost = request.POST.get('all_cost', 0)
        style = "宣传物资制作申请"

        # 修改时间格式
        time = request.POST.get('add_time', '')
        patten = '年|月'
        time = re.sub(patten, '-', time)
        time = re.sub('日', '', time)

        if title:
            draft_base = DraftBase()
            draft_base.title = title
            draft_base.status = status
            draft_base.style = style
            draft_base.add_time = time
            draft_base.draft_user = request.user
            draft_base.save()

            item_make = ItemsMake()
            item_make.remark = remark
            item_make.main = draft_base
            item_make.sum_cost = all_cost
            item_make.save()

            # 修改   保存接受人的id
            for a in accept_users:
                accept_user = UserProfile.objects.get(id=a)
                if accept_user:
                    draft_base.accept_user.add(accept_user)

            recall = {"status": "success", "lis_id": item_make.id}

            return HttpResponse(json.dumps(recall))

        return HttpResponse('{"status": "fail"}', content_type="application/json")


class ItemView(View):

    """
    物品信息
    """

    def post(self, request):

        lis_id = request.POST.get('lis_id', '')
        select = request.POST.get('select', '')
        item_name = request.POST.get('item_name', '')
        make_methed = request.POST.get('make_methed', '')
        time = request.POST.get('time', '')
        norm = request.POST.get('norm', '')
        unit = request.POST.get('unit', '')
        nums = request.POST.get('nums', 0)
        adv_name = request.POST.get('adv_name', '')
        adv_contact_person = request.POST.get('adv_contact_person', '')
        adv_contact_way = request.POST.get('adv_contact_way', '')
        cost = request.POST.get('cost', '')

        if lis_id and item_name:
            item = ItemMake()
            item.name = item_name
            item.category = select
            item.make_method = make_methed
            item.require_time = time
            item.standard = norm
            item.unit = unit
            item.nums = nums
            item.adv_com_name = adv_name
            item.adv_com_contact = adv_contact_person
            item.adv_com_mobile = adv_contact_way
            item.cost = cost
            item.lis_id = lis_id
            item.save()

            item_count = ItemMakeCount.objects.filter(user=request.user)
            if item_count:
                add_item_count = ItemMakeCount.objects.get(user=request.user)
                if select == '宣传（献血、知识）手册':
                    add_item_count.manual_count += 1
                    add_item_count.save()
                elif select == '电梯、海报广告	':
                    add_item_count.leaflet_count += 1
                    add_item_count.save()
                elif select == '电视媒体视频(材料)':
                    add_item_count.video_count += 1
                    add_item_count.save()
                elif select == '宣传、活动(指引)单张':
                    add_item_count.adv_count += 1
                    add_item_count.save()
                elif select == '其他':
                    add_item_count.other_count += 1
                    add_item_count.save()
            else:
                add_item_count = ItemMakeCount()
                add_item_count.user = request.user
                if select == '宣传（献血、知识）手册':
                    add_item_count.manual_count += 1
                    add_item_count.save()
                elif select == '电梯、海报广告	':
                    add_item_count.leaflet_count += 1
                    add_item_count.save()
                elif select == '电视媒体视频(材料)':
                    add_item_count.video_count += 1
                    add_item_count.save()
                elif select == '宣传、活动(指引)单张':
                    add_item_count.adv_count += 1
                    add_item_count.save()
                elif select == '其他':
                    add_item_count.other_count += 1
                    add_item_count.save()

            return HttpResponse('{"status": "success"}', content_type="application/json")

        return HttpResponse('{"status": "fail"}', content_type="application/json")


class ItemMakeFileUploadView(View):
    """
    宣传物资制作 文件上传
    """
    def post(self, request):
        lis_id = request.POST.get('lis_id', '')
        file = request.FILES.get("file", None)

        if file:
            item_make = ItemsMake.objects.get(id=lis_id)
            item_make.file = file
            item_make.save()

            return HttpResponse('{"status": "success"}', content_type="application/json")

        return HttpResponse('{"status": "fail"}', content_type="application/json")


class ItemReceiveView(LoginRequiredMixin, View):
    """
    宣传物资领用申请
    """
    def get(self, request):
        add_time = datetime.now()
        all_office = Office.objects.all()
        all_item = ItemMake.objects.filter(lis__main__status='已审批')

        return render(request, 'wzly_draft.html', {
            'add_time': add_time,
            "all_office": all_office,
            'all_item': all_item,
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

            remark = request.POST.get('remark', '')
            accept_users = request.POST.getlist('accept_user[]', [])
            style = request.POST.get('style', '')

            draft_base = DraftBase()
            draft_base.draft_user = request.user
            draft_base.title = title
            draft_base.status = status
            draft_base.add_time = time
            draft_base.style = style
            draft_base.save()

            receiver_draft = ItemsReceive()
            receiver_draft.remark = remark
            receiver_draft.main = draft_base
            receiver_draft.save()

            lis_draft_base = DraftBase.objects.get(id=draft_base.id)

            # 修改   保存接受人的id
            for a in accept_users:
                accept_user = UserProfile.objects.get(id=a)
                if accept_user:
                    lis_draft_base.accept_user.add(accept_user)

            recall = {"status": "success", "lis_id": receiver_draft.id}

            return HttpResponse(json.dumps(recall))

        return HttpResponse('{"status": "fail"}', content_type="application/json")


class ReceiveItemsView(LoginRequiredMixin, View):

    """
    宣传物资领用表 附属表 需要的领用的物资
    """

    def post(self, request):

        lis_id = request.POST.get('lis_id', '')
        name = request.POST.get('name', '')
        place = request.POST.get('place', '')
        count = request.POST.get('count', 0)
        direction = request.POST.get('direction', '')
        remark = request.POST.get('remark', '')
        if lis_id and name:
            need_item = NeedItem()
            need_item.name = name
            need_item.unit = place
            need_item.nums = count
            need_item.use_method = direction
            need_item.remark = remark
            need_item.lis_id = lis_id
            need_item.save()

            item_count = ItemReceiveCount.objects.filter(user=request.user)
            if item_count:
                add_item_count = ItemReceiveCount.objects.get(user=request.user)
                if name == '宣传手册':
                    add_item_count.manual_count += 1
                    add_item_count.save()
                elif name == '纪念胸章':
                    add_item_count.badge_count += 1
                    add_item_count.save()
                elif name == '样品吊坠':
                    add_item_count.pendant_count += 1
                    add_item_count.save()
                elif name == '电影票':
                    add_item_count.ticket_count += 1
                    add_item_count.save()
                elif name == '其他':
                    add_item_count.other_count += 1
                    add_item_count.save()
            else:
                add_item_count = ItemReceiveCount()
                add_item_count.user = request.user
                if name == '宣传手册':
                    add_item_count.manual_count += 1
                    add_item_count.save()
                elif name == '纪念胸章':
                    add_item_count.badge_count += 1
                    add_item_count.save()
                elif name == '样品吊坠':
                    add_item_count.pendant_count += 1
                    add_item_count.save()
                elif name == '电影票':
                    add_item_count.ticket_count += 1
                    add_item_count.save()
                elif name == '其他':
                    add_item_count.other_count += 1
                    add_item_count.save()

            return HttpResponse('{"status": "success"}', content_type="application/json")
        return HttpResponse('{"status": "fail"}', content_type="application/json")


class ItemReceiveDraftFileUploadView(View):

    """
    保存宣传信息起草表附件
    """

    def post(self, request, *args, **kwargs):

        lis_id = request.POST.get('lis_id', '')
        file = request.FILES.get("file", None)

        if file:
            item_receive = ItemsReceive.objects.get(id=lis_id)
            item_receive.file = file
            item_receive.save()

            return HttpResponse('{"status": "success"}', content_type="application/json")

        return HttpResponse('{"status": "fail"}', content_type="application/json")


class OverViewView(LoginRequiredMixin, View):
    """
    宣传概览
    """
    def get(self, request):

        all_plan = PropagatePlan.objects.filter(main__status='已审批')
        all_plan_count = all_plan.count()
        plan_1 = all_plan.filter(plan_style='宣传计划').count()
        plan_2 = all_plan.filter(plan_style='经济预算计划').count()
        plan_3 = all_plan.filter(plan_style='纪念品采购').count()
        plan_4 = all_plan.filter(plan_style='物料计划').count()
        all_scheme = Scheme.objects.filter(main__status='已审批')
        all_scheme_count = all_scheme.count()
        scheme1 = all_scheme.filter(category='普通宣传活动').count()
        scheme2 = all_scheme.filter(category='重大专项宣传活动').count()
        scheme3 = all_scheme.filter(category='固定献血者活动').count()
        scheme4 = all_scheme.filter(category='成分献血者活动').count()
        message_count = CategoryCount.objects.all()
        all_item = ItemMake.objects.filter(lis__main__status='已审批')
        all_item_receive = NeedItem.objects.all().count()
        make_by_self = all_item.filter(make_method='内部制作').count()
        make_by_adv = all_item.filter(make_method='广告公司制作').count()

        all_cost = 0
        for i in all_item:
            all_cost += i.cost

        tv_sum = 0
        inter_sum = 0
        lift_sum = 0
        news_sum = 0
        weibo_sum = 0
        other_sum = 0
        for c in message_count:
            tv_sum += c.tv_count
            inter_sum += c.internet_count
            lift_sum += c.lift_count
            news_sum += c.news_count
            weibo_sum += c.webo_count
            other_sum += c.other_count

        return render(request, 'Overview.html', {
            'all_plan_count': all_plan_count,
            'plan1': plan_1,
            'plan2': plan_2,
            'plan3': plan_3,
            'plan4': plan_4,
            'scheme1': scheme1,
            'scheme2': scheme2,
            'scheme3': scheme3,
            'scheme4': scheme4,
            'all_scheme_count': all_scheme_count,
            'tv_sum': tv_sum,
            'inter_sum': inter_sum,
            'lift_sum': lift_sum,
            'news_sum': news_sum,
            'weibo_sum': weibo_sum,
            'other_sum': other_sum,
            'all_item': all_item.count(),
            'all_cost': all_cost,
            'make_by_self': make_by_self,
            'make_by_adv': make_by_adv,
            'all_item_receive': all_item_receive
        })


class ReportQueryView(LoginRequiredMixin, View):
    """
    宣传工作总结报告查询
    """
    def get(self, request):

        return render(request, 'report_query.html', {})