from django.contrib import admin

from .models import MessageDraft, ObjMedia, Category, Opinion


admin.site.register(MessageDraft)
admin.site.register(ObjMedia)
admin.site.register(Category)
admin.site.register(Opinion)