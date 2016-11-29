from django.db import models
from django.contrib.auth.models import User

# Create your models here.

TK_STATUSES = (
    ('A', 'Active'),
    ('I', 'Inactive'),
)

CC_STATUSES = (
    ('O', 'Open'),
    ('C', 'Closed'),
)

class Timekeeper(models.Model):
    code = models.CharField(max_length=4, primary_key=True)
    first_name = models.CharField(max_length=12)
    middle_ini = models.CharField(max_length=2, blank = True)
    last_name = models.CharField(max_length=16)
    full_name = models.CharField(max_length=55)
    status = models.CharField(max_length=1, choices = TK_STATUSES)
    default_company = models.ForeignKey('Company', null=True, blank=True)

    def __str__(self):
        return u'%s - %s' % (self.code, self.full_name)

class Company(models.Model):
    code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=55)

    class Meta:
        verbose_name_plural ='companies'

    def __str__(self):
        return (self.name)

class Client(models.Model):
    code = models.CharField(max_length=7, primary_key=True)
    number = models.CharField(max_length=5)
    name = models.CharField(max_length=52)
    status = models.CharField(max_length=1, choices = CC_STATUSES)
    company = models.ForeignKey(Company)
    client_list_name = models.CharField(max_length=59)

    def __str__(self):
        return u'%s %s' % (self.name, self.code)

class Case(models.Model):
    code = models.CharField(max_length=12, primary_key=True)
    matter_id = models.CharField(max_length=10)
    number = models.CharField(max_length=5)
    name = models.CharField(max_length=52)
    status = models.CharField(max_length=1, choices = CC_STATUSES)
    client = models.ForeignKey(Client)
    company = models.ForeignKey(Company)
    case_list_name = models.CharField(max_length=59)

    def __str__(self):
        return u'%s %s' % (self.name, self.code)

class Activity(models.Model):
    code = models.CharField(max_length=2, primary_key=True)
    description = models.CharField(max_length=55)

    class Meta:
        verbose_name_plural ='activities'

    def __str__(self):
        return u'%s %s' % (self.code, self.description)

class Task(models.Model):
    set_code_code = models.CharField(max_length=5, primary_key=True)
    set_code = models.CharField(max_length=1)
    code = models.CharField(max_length=4)
    description = models.CharField(max_length=55)

    def __str__(self):
        return self.code


class Import_Log(models.Model):
    date_time = models.DateTimeField(auto_now=True)
    ran_by = models.CharField(max_length=39)
    results = models.TextField()

