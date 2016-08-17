from django.db import models
from django.contrib.auth.models import User
from climats.models import Timekeeper, Company, Activity, Client, Case, Task
from smart_selects.db_fields import ChainedForeignKey
from django.core.urlresolvers import reverse
from smart_selects.db_fields import ChainedForeignKey
from tlucidity.get_userobj import get_userobj

STATUSES = (
    ('O', 'Open'),
    ('R', 'Released'),
    ('E', 'Exported'),
)

class Entry(models.Model):
    user = models.ForeignKey(User, null=True)
    who = models.ForeignKey('climats.Timekeeper', verbose_name="Timekeeper", null=True)
    work_date = models.DateField(null=True)
    company = models.ForeignKey('climats.Company', null=True)
    matter = models.CharField(max_length=10, null=True)
    client = ChainedForeignKey(
        'climats.Client',
        chained_field="company",
        chained_model_field="company",
        show_all=False,
        null=True
    )
    case = ChainedForeignKey(
        'climats.Case',
        chained_field="client",
        chained_model_field="client",
        show_all=False,
        null=True
    )
    activity_code1 = models.ForeignKey('climats.Activity', related_name = 'acode1', null=True, blank=True)
    activity_code2 = models.ForeignKey('climats.Activity', related_name = 'acode2', null=True, blank=True)
    hours = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    narrative = models.TextField(blank=True)
    created_date = models.DateField(auto_now=True,null=True)
    last_change_date = models.DateField(auto_now=True, null=True, blank=True)
    released_date = models.DateField(null=True, blank=True)
    exported_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUSES, default='O')
    released = models.BooleanField(default=False)
    exported = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural ='entries'

    def __str__(self):
        return u'%s, %s, %s, %s, %s' % (self.who.code, self.work_date.strftime("%m/%d/%y"), self.company.code, self.matter, self.hours)

    def get_absolute_url(self):
        return reverse('entry-view', kwargs={'pk': self.id})

    def _get_matter(self):
        fullstring = self.case.code
        clp = fullstring[2:7]
        sstring = clp + '-' + fullstring[7:11]
        return sstring
    matter = property(_get_matter)

    def save(self, *args, **kwargs):
        usero = get_userobj()
        usobj = User.objects.get(pk=usero.pk)
        self.user = usobj
        if not self.pk:
            self.who = Profile.objects.get(user_id=usobj.id).for_whom
        super(Entry, self).save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User)
    for_whom = models.ForeignKey('climats.Timekeeper', verbose_name='entering for', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('setk', kwargs={'pk': self.id})

    def __str__(self):
        return self.user.username
