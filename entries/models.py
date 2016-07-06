from django.db import models
from django.contrib.auth.models import User
from climats.models import Timekeeper, Company, Activity, Client, Case, Task
from django.core.urlresolvers import reverse

STATUSES = (
    ('O', 'Open'),
    ('R', 'Released'),
    ('E', 'Exported'),
)

class Entry(models.Model):
    user = models.ForeignKey(User)
    who = models.ForeignKey('climats.Timekeeper', null=True)
    work_date = models.DateField(null=True)
    company = models.ForeignKey('climats.Company', null=True)
    matter = models.CharField(max_length=10, null=True)
    client = models.ForeignKey('climats.Client', null=True)
    case = models.ForeignKey('climats.Case', null=True)
    activity_code1 = models.ForeignKey('climats.Activity', related_name = 'acode1', null=True, blank=True)
    activity_code2 = models.ForeignKey('climats.Activity', related_name = 'acode2', null=True, blank=True)
    hours = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    narrative = models.TextField(blank=True)
    created_date = models.DateField(null=True)
    last_change_date = models.DateField(auto_now=True, null=True, blank=True)
    released_date = models.DateField(null=True, blank=True)
    exported_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUSES, default='O')

    class Meta:
        verbose_name_plural ='entries'

    def __str__(self):
        return self.matter

    def get_absolute_url(self):
        return reverse('entry-view', kwargs={'pk': self.id})


class Profile(models.Model):
    user = models.OneToOneField(User)
    for_whom = models.ForeignKey('climats.Timekeeper', verbose_name='entering for', null=True, blank=True)

    def get_tk_info(user):
        return Profile.objects.get(user=user)

    def get_absolute_url(self):
        return reverse('setk', kwargs={'pk': self.id})

    def __str__(self):
        return self.user.username
