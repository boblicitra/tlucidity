# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-05-02 22:37
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0002_auto_20170502_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expthru',
            name='key_list',
            field=models.CommaSeparatedIntegerField(blank=True, max_length=32768, null=True),
        ),
        migrations.AlterField(
            model_name='expthru',
            name='thru_date',
            field=models.DateField(default=datetime.datetime(2017, 5, 2, 22, 37, 54, 655426), verbose_name='Through Date'),
        ),
    ]
