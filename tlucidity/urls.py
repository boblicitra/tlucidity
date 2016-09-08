"""tlucidity URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, patterns, include
from django.contrib import admin

from climats import views
from entries import views, auth

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^$', views.index, name = 'index'),
    url(r'^entrylist/', views.ListEntryView, name = 'entry-list'),
    url(r'^makentry/', views.MakeEntryView.as_view(), name = 'make-entry'),
    url(r'^(?P<pk>\d+)/$', views.EntryView.as_view(), name = 'entry-view'),
    url(r'^(\d+)/$', views.EntryView.as_view(), name = 'entry-detail'),
    url(r'^edit/(?P<pk>\d+)/$', views.UpdateEntryView.as_view(), name = 'entry-edit'),
    url(r'^delete/(?P<pk>\d+)/$', views.DeleteEntryView.as_view(), name = 'delete-entry'),
    url(r'^editw/(?P<pk>\d+)/$', views.SelectTkView.as_view(), name = 'set-w'),
    url(r'^editw/', views.SelectTkView.as_view(), name = 'set-w'),
    url(r'^dashboard/', views.OneTkEntryView, name = 'dashboard'),
    url(r'^setk/$', views.SeeTk, name = 'setk'),
    url(r'^releaselist/', views.ReleaseView, name = 'release-list'),
    url(r'^release/$', views.Release, name = 'release'),
    url(r'^released/$', views.Released, name = 'released'),
    url(r'^login/', auth.login, name = 'login'),
    url(r'^logout/', auth.logout, name = 'logout'),
    url(r'^register/', auth.register, name = 'register'),
    url('',include('climats.urls')),
]
