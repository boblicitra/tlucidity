from django.contrib import admin

from .models import *

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('code','name',)
    
class TimekeeperAdmin(admin.ModelAdmin):
    list_display = ('code','last_name','first_name','status',)
    list_display_link = ('code',)
    list_filter = ('status',)

class ClientAdmin(admin.ModelAdmin):
    list_display = ('code','name','status',)
    list_display_link = ('code',)
    list_filter = ('status', 'company',)

class CaseAdmin(admin.ModelAdmin):
    list_display = ('code','name','status',)
    list_display_link = ('code',)
    list_filter = ('status', 'company',)

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('code','description',)
    list_display_link = ('code',)

class TaskAdmin(admin.ModelAdmin):
    list_display = ('code','description',)
    list_display_link = ('code',)

class Import_LogAdmin(admin.ModelAdmin):
    list_display = ('date_time','ran_by',)
    list_display_link = ('date_time',)

admin.site.register(Company,CompanyAdmin)

admin.site.register(Timekeeper,TimekeeperAdmin)

admin.site.register(Client,ClientAdmin)

admin.site.register(Case,CaseAdmin)

admin.site.register(Activity,ActivityAdmin)

admin.site.register(Task,TaskAdmin)

admin.site.register(Import_Log,Import_LogAdmin)
