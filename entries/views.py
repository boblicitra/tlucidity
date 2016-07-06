from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import *
from rest_framework import viewsets
from django.core.urlresolvers import reverse
from django.http import HttpResponse
#from django.contrib.auth.mixins import LoginRequiredMixin
from entries.models import Entry
from entries.models import Profile


class OneTkEntryView(ListView):
    
    model = Entry
    template_name = 'entries/tk_entry_list.html'

class ListEntryView(ListView):
    
    model = Entry
    template_name = 'entries/entry_list.html'

class EntryView(DetailView):
    
    model = Entry
    fields = ['who', 'work_date', 'company', 'matter', 'hours','narrative']
    template_name = 'entries/entry.html'

    def get_success_url(self):
        return reverse('entry-list')


def index(request):
    return render(request, 'index.html')


class MakeEntryView(CreateView):
    
    model = Entry
    fields = ['who', 'work_date', 'company', 'matter', 'hours','narrative']
    template_name = 'entries/make_entry.html'

    def get_success_url(self):
        return reverse('entry-list')

class UpdateEntryView(UpdateView):
    
    model = Entry
    fields = ['who', 'work_date', 'company', 'matter', 'hours','narrative']
    template_name = 'entries/make_entry.html'

    def get_success_url(self):
        return reverse('dashboard')

class DeleteEntryView(DeleteView):
    
    model = Entry
    fields = ['who', 'work_date', 'company', 'matter', 'hours','narrative']
    template_name = 'entries/delete_entry.html'

    def get_success_url(self):
        return reverse('dashboard')

class SetTimekeeper(UpdateView):
    
    model = Profile
    fields = ['for_whom']
    template_name = 'entries/set_tki.html'

    def get_success_url(self):
        return reverse('dashboard')


def SetTk(request):

    content = ''
    for profile in Profile.objects.all():
        content += 'maybe???????  '

    return HttpResponse(content)
