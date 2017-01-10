from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from climats.models import Timekeeper, Company, Activity, Client, Case, Task
from smart_selects.db_fields import ChainedForeignKey
from django.http import request
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
    who = models.ForeignKey('climats.Timekeeper', verbose_name="Timekeeper", null=True, blank=True)
    work_date = models.DateField(null=True)
    company = models.ForeignKey('climats.Company', blank=True)
    matter = models.CharField(max_length=10, null=True)
    client = ChainedForeignKey(
        'climats.Client',
        chained_field="company",
        chained_model_field="company",
        limit_choices_to={'status':'O'},
        show_all=False,
        null=True,
        blank=True
    )
    case = ChainedForeignKey(
        'climats.Case',
        chained_field="client",
        chained_model_field="client",
        limit_choices_to={'status':'O'},
        show_all=False,
        auto_choose=True,
        null=True,
        blank=True
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
    recent_files = models.ForeignKey('Matter_use', null=True, blank=True, help_text='Select a recent file to override company, client & case')
    matter_keyin = models.CharField(max_length=10, null=True, blank=True, verbose_name="Matter", help_text='Type a client-case number to override client and case')

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
        usobj = get_userobj()
        self.user = usobj
        self.matter_keyin = ''
        exported_date = ''
        if not self.who:
            self.who = Profile.objects.get(user_id=usobj.id).for_whom
            self.recent_files = None
            if self.released == True:
                self.status = 'R'
                self.released_date = datetime.now()
            super(Entry, self).save(*args, **kwargs)
            Profile.objects.filter(user_id=usobj.id).update(mre_date=self.work_date)
            rm_id = self.who.code + self.case.code
            rm_who = self.who
            rm_case = self.case
            rm_days = Profile.objects.get(user_id=usobj.id).recent_days
            if Matter_use.objects.filter(worker_case=rm_id).exists():
                Matter_use.objects.filter(worker_case=rm_id).update(last_used=datetime.now())
            else:
                Matter_use.objects.create(worker_case=rm_id, timekeeper=rm_who, matter=rm_case, last_used=datetime.now())
            for used_case in Matter_use.objects.filter(timekeeper=rm_who):
                diff = datetime.now().date() - used_case.last_used 
                if diff.days > rm_days:
                    Matter_use.delete(used_case) 
        else:
#           ('who already set - updating existing')
            self.last_change_date = datetime.now()
            self.recent_files = None
            if self.released == True:
                if self.released_date == None:
                    self.status = 'R'
                    self.released_date = datetime.now()
            else:
                self.status = 'O'
                self.released_date = None
            super(Entry, self).save(*args, **kwargs)
        return reverse('dashboard')


class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    for_whom = models.ForeignKey('climats.Timekeeper', limit_choices_to={'status':'A'}, verbose_name='entering for', null=True, blank=True)
    mre_date = models.DateField(null=True, blank=True)
    recent_days = models.IntegerField(default=15, verbose_name='Days', help_text='until files deleted from recent files list.')

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('set-w', kwargs={'pk': self.user.id})


class Matter_use(models.Model):
    worker_case = models.CharField(max_length=15, primary_key=True)
    timekeeper = models.ForeignKey('climats.Timekeeper', limit_choices_to={'status':'A'})
    matter = models.ForeignKey('climats.Case', limit_choices_to={'status':'O'})
    last_used = models.DateField()

    def __str__(self):
        return u'%s %s(%s) %s(%s) ' % (self.matter.company.code, self.matter.client.name, self.matter.client.number, self.matter.name, self.matter.number)


class Expthru(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    thru_date = models.DateField(default=datetime.now(), verbose_name="Through Date")
    key_list = models.CommaSeparatedIntegerField(max_length=4096, null=True, blank=True)

    def save(self, *args, **kwargs):
        usobj = get_userobj()
        self.user = usobj
        super(Expthru, self).save(*args, **kwargs)
        return reverse('dashboard')


class Export_Error(models.Model):
    date_time = models.DateTimeField(auto_now=True)
    ran_by = models.CharField(max_length=39)
    results = models.TextField()

