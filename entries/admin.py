from django.contrib import admin

from .models import *

class EntryAdmin(admin.ModelAdmin):
    list_display = ('who','matter','work_date','hours','status',)
    list_filter = ('status',)

admin.site.register(Entry,EntryAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','for_whom',)

admin.site.register(Profile,ProfileAdmin)
