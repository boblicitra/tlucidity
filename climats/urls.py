"""climats URL Configuration
"""
from django.conf.urls import url, patterns, include
from climats import views

urlpatterns = [
    url(r'^timeadmin/$', views.timeadmin, name = 'timeadmin'),
    url(r'^timeadmin/updatevals$', views.updatevals, name = 'updatevals'),
    url(r'^timeadmin/updateval$', views.updateval, name = 'updateval'),
    url(r'^timeadmin/exporttime$', views.ExportEntryView.as_view(), name = 'export-time'),
]
