# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-27 07:41
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0005_auto_20160927_0740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expthru',
            name='thru_date',
            field=models.DateField(default=datetime.datetime(2016, 9, 27, 7, 41, 26, 881475), verbose_name='Through Date'),
        ),
    ]