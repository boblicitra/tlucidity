from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import *
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django_tables2 import RequestConfig
from entries.forms import EntryForm, EntryEditForm, SetTkForm
from entries.models import Entry, Profile
from entries.tables import DashTable, FullTable, OneTkTable
from entries.tables import ForReleaseTable, SelectedRelTable
from climats.models import Timekeeper
from datetime import datetime
from django.contrib.auth.models import User
from django.template.response import TemplateResponse
from tlucidity.get_userobj import get_userobj


def ReleaseView(request):
    usobj = get_userobj()
    selected_tk=Profile.objects.get(user = usobj).for_whom
    table = ForReleaseTable(Entry.objects.filter(who=selected_tk, status='O').order_by('work_date'))
    RequestConfig(request, paginate={'per_page': 345}).configure(table)
    whom = selected_tk
    return render(request, 'entries/release_list.html', {'table': table, 'whom': whom})


def Release(request):
    count = 0
    num_hours = 0
    if request.method == 'POST':
        if 'selection' in request.POST: 
            ent_list = request.POST.getlist('selection')
            ei = 0
            while ei < len(ent_list):
                epk = int(ent_list[ei])
                selected = Entry.objects.get(pk=epk)
                count = count + 1
                num_hours = num_hours + selected.hours 
                ei = ei + 1
            table = SelectedRelTable(Entry.objects.filter(pk__in=ent_list).order_by('work_date'))
            RequestConfig(request, paginate={'per_page': 345}).configure(table)
            return render(request, 'entries/release.html', {'count': count, 'hours': num_hours, 'table': table})
        return render(request, 'entries/release.html', {'count': count, 'hours': num_hours})
    return render(request, 'entries/release.html', {'count': count})


def Released(request):
    count = 0
    num_hours = 0
    if request.method == 'POST':
        if 'selection' in request.POST: 
            ent_list = request.POST.getlist('selection')
            ei = 0
            right_now = datetime.now()
            while ei < len(ent_list):
                epk = int(ent_list[ei])
                selected = Entry.objects.get(pk=epk)
                count = count + 1
                num_hours = num_hours + selected.hours 
                Entry.objects.filter(id=epk).update(status='R')
                Entry.objects.filter(id=epk).update(released_date=right_now)
                Entry.objects.filter(id=epk).update(released=True)
                ei = ei + 1
            return render(request, 'entries/released.html',
                {'count': count, 'hours': num_hours}
        )
        return render(request, 'entries/released.html', {'count': count})
    return render(request, 'entries/released.html', {'count': count})


def ListEntryView(request):
    usobj = get_userobj()
    selected_tk=Profile.objects.get(user = usobj).for_whom
    table = OneTkTable(Entry.objects.filter(who=selected_tk).order_by('work_date'))
    RequestConfig(request, paginate={'per_page': 100}).configure(table)
    whom = selected_tk
    return render(request, 'entries/entry_list.html', {'table': table, 'whom': whom})


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
    form_class = EntryEditForm
    template_name = 'entries/edit_entry.html'

    def get_success_url(self):
        return reverse('dashboard')

    def get_context_data(self, **kwargs):
        context = super(UpdateEntryView, self).get_context_data(**kwargs)
        usobj = get_userobj()
        selected_tk=Profile.objects.get(user = usobj).for_whom
        context['whom'] = selected_tk
        context['stat'] = self.object.status
        return context


class SelectTkView(UpdateView):
    
    model = Profile
    form_class = SetTkForm
    template_name = 'entries/set_tki.html'

    def get_success_url(self):
        return reverse('set-w')

    def get_context_data(self, **kwargs):
        context = super(SelectTkView, self).get_context_data(**kwargs)
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


def SeeTk(request):
    if request.method == 'POST':
        form = SetTkForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save(force_update=True, force_insert=False)
            usobj = get_userobj()
            selected_tk=Profile.objects.get(user = usobj).for_whom
            return TemplateResponse(request, 'entries/check_tk.html', {'for_whom' : selected_tk,})
    else:
        form = SetTkForm()
        usobj = get_userobj()
        selected_tk=Profile.objects.get(user = usobj).for_whom
    return TemplateResponse(request, 'entries/check_tk.html', {'for_whom' : selected_tk,})


def OneTkEntryView(request):
    usobj = get_userobj()
    selected_tk=Profile.objects.get(user = usobj).for_whom
    full_list = Entry.objects.filter(who=selected_tk).exclude(status='E')
#   full_list = Entry.objects.filter(who=selected_tk)
    dates=list()
    for ent in full_list:
        if dates.count(ent.work_date)==0:
            dates.append(ent.work_date)
    dates.sort()
    if len(dates)>0:
        tabdate = dates[0]
    else:
        tabdate = '1959-08-23'
    table1 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>1:
        tabdate = dates[1]
    else:
        tabdate = '1959-08-23'
    table2 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>2:
        tabdate = dates[2]
    else:
        tabdate = '1959-08-23'
    table3 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>3:
        tabdate = dates[3]
    else:
        tabdate = '1959-08-23'
    table4 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>4:
        tabdate = dates[4]
    else:
        tabdate = '1959-08-23'
    table5 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>5:
        tabdate = dates[5]
    else:
        tabdate = '1959-08-23'
    table6 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>6:
        tabdate = dates[6]
    else:
        tabdate = '1959-08-23'
    table7 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>7:
        tabdate = dates[7]
    else:
        tabdate = '1959-08-23'
    table8 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>8:
        tabdate = dates[8]
    else:
        tabdate = '1959-08-23'
    table9 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>9:
        tabdate = dates[9]
    else:
        tabdate = '1959-08-23'
    table10 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>10:
        tabdate = dates[10]
    else:
        tabdate = '1959-08-23'
    table11 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>11:
        tabdate = dates[11]
    else:
        tabdate = '1959-08-23'
    table12 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>12:
        tabdate = dates[12]
    else:
        tabdate = '1959-08-23'
    table13 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>13:
        tabdate = dates[13]
    else:
        tabdate = '1959-08-23'
    table14 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>14:
        tabdate = dates[14]
    else:
        tabdate = '1959-08-23'
    table15 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>15:
        tabdate = dates[15]
    else:
        tabdate = '1959-08-23'
    table16 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>16:
        tabdate = dates[16]
    else:
        tabdate = '1959-08-23'
    table17 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>17:
        tabdate = dates[17]
    else:
        tabdate = '1959-08-23'
    table18 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>18:
        tabdate = dates[18]
    else:
        tabdate = '1959-08-23'
    table19 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>19:
        tabdate = dates[19]
    else:
        tabdate = '1959-08-23'
    table20 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>20:
        tabdate = dates[20]
    else:
        tabdate = '1959-08-23'
    table21 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>21:
        tabdate = dates[21]
    else:
        tabdate = '1959-08-23'
    table22 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>22:
        tabdate = dates[22]
    else:
        tabdate = '1959-08-23'
    table23 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>23:
        tabdate = dates[23]
    else:
        tabdate = '1959-08-23'
    table24 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>24:
        tabdate = dates[24]
    else:
        tabdate = '1959-08-23'
    table25 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>25:
        tabdate = dates[25]
    else:
        tabdate = '1959-08-23'
    table26 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>26:
        tabdate = dates[26]
    else:
        tabdate = '1959-08-23'
    table27 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>27:
        tabdate = dates[27]
    else:
        tabdate = '1959-08-23'
    table28 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>28:
        tabdate = dates[28]
    else:
        tabdate = '1959-08-23'
    table29 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>29:
        tabdate = dates[29]
    else:
        tabdate = '1959-08-23'
    table30 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>30:
        tabdate = dates[30]
    else:
        tabdate = '1959-08-23'
    table31 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>31:
        tabdate = dates[31]
    else:
        tabdate = '1959-08-23'
    table32 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>32:
        tabdate = dates[32]
    else:
        tabdate = '1959-08-23'
    table33 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>33:
        tabdate = dates[33]
    else:
        tabdate = '1959-08-23'
    table34 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>34:
        tabdate = dates[34]
    else:
        tabdate = '1959-08-23'
    table35 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>35:
        tabdate = dates[35]
    else:
        tabdate = '1959-08-23'
    table36 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>36:
        tabdate = dates[36]
    else:
        tabdate = '1959-08-23'
    table37 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>37:
        tabdate = dates[37]
    else:
        tabdate = '1959-08-23'
    table38 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>38:
        tabdate = dates[38]
    else:
        tabdate = '1959-08-23'
    table39 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
    if len(dates)>39:
        tabdate = dates[39]
    else:
        tabdate = '1959-08-23'
    table40 = DashTable(Entry.objects.filter(who=selected_tk, work_date=tabdate).order_by('client_id'))
#    RequestConfig(request).configure(table)
    whom = selected_tk
    pro_id=Profile.objects.get(user = usobj).user.id
    profile_pk = pro_id
    if usobj.groups.filter(name='Proxy').exists():
        swtk = 'can'
    else:
        swtk = 'cannot'
    return render(request, 'entries/tk_entry_list.html', {
        'table1': table1, 
        'table2': table2, 
        'table3': table3, 
        'table4': table4, 
        'table5': table5, 
        'table6': table6, 
        'table7': table7, 
        'table8': table8, 
        'table9': table9, 
        'table10': table10, 
        'table11': table11, 
        'table12': table12, 
        'table13': table13, 
        'table14': table14, 
        'table15': table15, 
        'table16': table16, 
        'table17': table17, 
        'table18': table18, 
        'table19': table19, 
        'table20': table20, 
        'table21': table21, 
        'table22': table22, 
        'table23': table23, 
        'table24': table24, 
        'table25': table25, 
        'table26': table26, 
        'table27': table27, 
        'table28': table28, 
        'table29': table29, 
        'table30': table30, 
        'table31': table31, 
        'table32': table32, 
        'table33': table33, 
        'table34': table34, 
        'table35': table35, 
        'table36': table36, 
        'table37': table37, 
        'table38': table38, 
        'table39': table39, 
        'table40': table40, 
        'profile_pk': profile_pk, 
        'swtk': swtk, 
        'whom': whom
    })
