# _*_ coding:utf-8 _*_

from django import forms

from .models import MessageDraft

__author__ = 'haoSev7'
__date__ = '2017/5/26 21:30'


class MessageDraftForm(forms.ModelForm):

    class Meta:
        model = MessageDraft
        fields = ['draft_user', 'title', 'content', 'remark', 'start_time', 'end_time', 'media', 'file']