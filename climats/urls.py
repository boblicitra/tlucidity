"""climats URL Configuration
"""
from django.conf.urls import url, patterns, include
from climats import views

urlpatterns = [
    url(r'^timeadmin/$', views.timeadmin, name = 'timeadmin'),
    url(r'^timeadmin/updatevals$', views.updatevals, name = 'updatevals'),
    url(r'^timeadmin/updateval$', views.updateval, name = 'updateval'),
    url(r'^timeadmin/exported$', views.Exported, name = 'exported'),
    url(r'^timeadmin/exportlist$', views.Exportlist, name = 'export-list'),
    url(r'^timeadmin/exports/', views.ExpthrView.as_view(), name = 'exports'),
]
