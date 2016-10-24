# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-04 04:23
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0016_auto_20161004_0228'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='recent_files',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
        migrations.AlterField(
            model_name='expthru',
            name='thru_date',
            field=models.DateField(default=datetime.datetime(2016, 10, 4, 4, 23, 40, 234922), verbose_name='Through Date'),
        ),
    ]