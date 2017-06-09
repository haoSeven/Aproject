# _*_ coding:utf-8 _*_

from django import forms

from .models import MessageDraft

__author__ = 'haoSev7'
__date__ = '2017/5/26 21:30'


class MessageDraftFileUploadForm(forms.ModelForm):

    class Meta:
        model = MessageDraft
        fields = ['file']
