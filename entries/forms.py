from django import forms
from django.forms import ModelForm
from django.contrib.admin.widgets import AdminDateWidget
from django.core.exceptions import ValidationError
from entries.models import Entry
from entries.models import Profile
from tlucidity.get_userobj import get_userobj

class EntryForm(ModelForm):
    work_date = forms.DateField(error_messages={'required': 'Enter a date'})    

    class Meta:
        model = Entry
        fields = ['who', 'work_date', 'company', 'client', 'case', 'hours', 'activity_code1', 'activity_code2', 'narrative', 'released']
        widgets = {
            'narrative' : forms.Textarea(attrs={'rows':5, 'cols':70,}),
            'who' : forms.HiddenInput(),
        }

class EntryEditForm(ModelForm):

    class Meta:
        model = Entry
        fields = ['id', 'who', 'work_date', 'company', 'client', 'case', 'hours', 'activity_code1', 'activity_code2', 'narrative', 'released', 'released_date']
        widgets = {
            'narrative' : forms.Textarea(attrs={'rows':5, 'cols':70,}),
            'who' : forms.HiddenInput(),
            'released_date' : forms.HiddenInput(),
        }


class SetTkForm(ModelForm):

    class Meta:
        model = Profile
        fields = ['for_whom']
