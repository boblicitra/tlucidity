from django.contrib import admin

from .models import *

class EntryAdmin(admin.ModelAdmin):
    list_display = ('who','matter','work_date','hours','status',)
    list_filter = ('status', 'who', 'company', 'exported_date')

admin.site.register(Entry,EntryAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','for_whom','recent_days',)

admin.site.register(Profile,ProfileAdmin)


class ExportErrorAdmin(admin.ModelAdmin):
    list_display = ('date_time','ran_by',)
    list_display_link = ('date_time',)

admin.site.register(Export_Error,ExportErrorAdmin)


class MatterUseAdmin(admin.ModelAdmin):
    list_display = ('timekeeper','matter','last_used',)
    list_filter = ('timekeeper',)

admin.site.register(Matter_use,MatterUseAdmin)

