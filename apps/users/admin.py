from django.contrib import admin

from .models import UserProfile, Department, Office, Team


admin.site.register(UserProfile)
admin.site.register(Department)
admin.site.register(Office)
admin.site.register(Team)