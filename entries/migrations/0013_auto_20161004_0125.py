# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-04 01:25
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0012_auto_20161004_0125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expthru',
            name='thru_date',
            field=models.DateField(default=datetime.datetime(2016, 10, 4, 1, 25, 53, 250238), verbose_name='Through Date'),
        ),
        migrations.AlterField(
            model_name='matter_use',
            name='last_used',
            field=models.DateField(default=datetime.datetime(2016, 10, 4, 1, 25, 53, 249671)),
        ),
    ]
