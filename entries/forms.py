from django import forms
from django.forms import ModelForm
from functools import partial
from django.core.exceptions import ValidationError
from entries.models import Entry
from entries.models import Profile, Expthru, Matter_use
from climats.models import Company, Client, Case
from django.contrib.auth.models import User
from tlucidity.get_userobj import get_userobj

class EntryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EntryForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            usobj = get_userobj()
            worker = Profile.objects.get(user_id=usobj.id).for_whom
            self.fields['recent_files'].queryset = Matter_use.objects.filter(timekeeper=worker).order_by('matter')
            self.fields['recent_files'].widget.attrs.update({'onchange':'recent()'})

    def get_mre_date():
        usobj = get_userobj()
        return Profile.objects.get(user_id=usobj.id).mre_date
        
    work_date = forms.DateField(initial=get_mre_date, widget=forms.DateInput(attrs={'class':'datepicker', 'id':'datepicker'}))

    class Meta:
        model = Entry
        fields = ['who', 'work_date', 'recent_files', 'company', 'client', 'case', 'hours', 'activity_code1', 'activity_code2', 'narrative', 'released']
        widgets = {
            'narrative' : forms.Textarea(attrs={'rows':5, 'cols':70,}),
	    'who' : forms.HiddenInput(),
            'hours' : forms.NumberInput(attrs={'min': 0, 'step': 0.1}),
        }

    def clean_company(self):
        compf = self.cleaned_data['company']
        if compf is None:
            recentdata = self.cleaned_data['recent_files']
            if recentdata is not None:
                all4 = recentdata.worker_case
                lall = len(all4)
                s1 = lall - 11
                s2 = lall - 9
                compcode = all4[s1:s2]
                compf = Company.objects.get(code=compcode)
        if compf is None:
            raise forms.ValidationError("You must select a company")
        return compf

    def clean_client(self):
        clif = self.cleaned_data['client']
        if clif is None:
            recentdata = self.cleaned_data['recent_files']
            if recentdata is not None:
                all4 = recentdata.worker_case
                lall = len(all4)
                s1 = lall - 11
                s2 = lall - 4
                clientcode = all4[s1:s2]
                clif = Client.objects.get(code=clientcode)
        if clif is None:
            raise forms.ValidationError("You must select a client")
        return clif


    def clean_case(self):
        casef = self.cleaned_data['case']
        if casef is None:
            recentdata = self.cleaned_data['recent_files']
            if recentdata is not None:
                casef = recentdata.matter
        if casef is None:
            raise forms.ValidationError("You must select a case")
        return casef


class EntryEditForm(ModelForm):

    work_date = forms.DateField(widget=forms.DateInput(attrs={'class':'datepicker', 'id':'datepicker'}))

    class Meta:
        model = Entry
        fields = ['id', 'who', 'work_date', 'company', 'client', 'case', 'hours', 'activity_code1', 'activity_code2', 'narrative', 'released', 'released_date']
        widgets = {
            'narrative' : forms.Textarea(attrs={'rows':5, 'cols':70,}),
            'who' : forms.HiddenInput(),
            'released_date' : forms.HiddenInput(),
            'hours' : forms.NumberInput(attrs={'min': 0, 'step': 0.1}),
        }


class SetTkForm(ModelForm):

    class Meta:
        model = Profile
        fields = ['for_whom', 'recent_days']

        widgets = {
            'recent_days' : forms.NumberInput(attrs={'min': 8, 'step': 1}),
        }


class ExpthruForm(ModelForm):

    thru_date = forms.DateField(widget=forms.DateInput(attrs={'class':'datepicker', 'id':'datepicker'}))
    class Meta:
        model = Expthru
        fields = ['thru_date']
