# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-24 16:06
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expthru',
            name='thru_date',
            field=models.DateField(default=datetime.datetime(2016, 9, 24, 16, 6, 40, 999912), verbose_name='Through Date'),
        ),
    ]