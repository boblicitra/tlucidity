# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-12 23:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0013_remove_entry_matter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='user',
        ),
    ]
