from django import forms
from django.core.exceptions import ValidationError

from entries.models import Entry

class EntryForm(forms.ModelForm):

    class Meta:
        model = Entry
        fields = ['who', 'work_date', 'company', 'matter']

