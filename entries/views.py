from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import *
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from entries.forms import EntryForm
from entries.models import Entry
from entries.models import Profile
from climats.models import Timekeeper
from django.contrib.auth.models import User
from django.template.response import TemplateResponse
from tlucidity.get_userobj import get_userobj

class OneTkEntryView(ListView):
    
    model = Entry
    template_name = 'entries/tk_entry_list.html'

    def get_queryset(self):
        usobj = get_userobj()
        selected_tk=Profile.objects.get(user = usobj).for_whom
        qlist =  Entry.objects.filter(who=selected_tk, status = 'O').order_by('work_date')
        return qlist

    def get_context_data(self, **kwargs):
        context = super(OneTkEntryView, self).get_context_data(**kwargs)
        usobj = get_userobj()
        selected_tk=Profile.objects.get(user = usobj).for_whom
        context['whom'] = selected_tk
        return context


class ListEntryView(ListView):
    
    model = Entry
    template_name = 'entries/entry_list.html'

class EntryView(DetailView):
    
    model = Entry
    fields = ['who', 'work_date', 'company', 'client', 'case', 'matter', 'hours','narrative']
    template_name = 'entries/entry.html'

    def get_success_url(self):
        return reverse('entry-list')


def index(request):
    return render(request, 'index.html')


class MakeEntryView(CreateView):
    
    form_class = EntryForm
    template_name = 'entries/make_entry.html'

    def get_success_url(self):
        return reverse('make-entry')

    def get_context_data(self, **kwargs):
        context = super(MakeEntryView, self).get_context_data(**kwargs)
        usobj = get_userobj()
        selected_tk=Profile.objects.get(user = usobj).for_whom
        context['whom'] = selected_tk
        return context


class UpdateEntryView(UpdateView):
    
    model = Entry
    form_class = EntryForm
    template_name = 'entries/make_entry.html'

    def get_success_url(self):
        return reverse('dashboard')

    def get_context_data(self, **kwargs):
        context = super(UpdateEntryView, self).get_context_data(**kwargs)
        usobj = get_userobj()
        selected_tk=Profile.objects.get(user = usobj).for_whom
        context['whom'] = selected_tk
        return context


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
    usobj = get_userobj()
    selected_tk=Profile.objects.get(user = usobj).for_whom
    if usobj.groups.filter(name='Proxy').exists():
        proxy = 'can'
    else:
        proxy = 'cannot'
    return TemplateResponse(request, 'entries/check_tk.html', {'for_whom' : selected_tk, 'changeyn' : proxy})
