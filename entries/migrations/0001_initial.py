# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-05-02 20:06
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('climats', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_date', models.DateField(null=True)),
                ('hours', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('narrative', models.TextField(blank=True)),
                ('created_date', models.DateField(auto_now=True, null=True)),
                ('last_change_date', models.DateField(auto_now=True, null=True)),
                ('released_date', models.DateField(blank=True, null=True)),
                ('exported_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('O', 'Open'), ('R', 'Released'), ('E', 'Exported')], default='O', max_length=1)),
                ('released', models.BooleanField(default=False)),
                ('exported', models.BooleanField(default=False)),
                ('matter_keyin', models.CharField(blank=True, help_text='Type a client-case number to override client and case', max_length=10, null=True, verbose_name='Matter')),
                ('activity_code1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='acode1', to='climats.Activity')),
                ('activity_code2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='acode2', to='climats.Activity')),
                ('case', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, blank=True, chained_field='client', chained_model_field='client', null=True, on_delete=django.db.models.deletion.CASCADE, to='climats.Case')),
                ('client', smart_selects.db_fields.ChainedForeignKey(blank=True, chained_field='company', chained_model_field='company', null=True, on_delete=django.db.models.deletion.CASCADE, to='climats.Client')),
                ('company', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='climats.Company')),
            ],
            options={
                'verbose_name_plural': 'entries',
            },
        ),
        migrations.CreateModel(
            name='Export_Error',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(auto_now=True)),
                ('ran_by', models.CharField(max_length=39)),
                ('results', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Expthru',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('thru_date', models.DateField(default=datetime.datetime(2017, 5, 2, 20, 6, 15, 991374), verbose_name='Through Date')),
                ('key_list', models.CommaSeparatedIntegerField(blank=True, max_length=23, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Matter_use',
            fields=[
                ('worker_case', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('last_used', models.DateField()),
                ('matter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='climats.Case')),
                ('timekeeper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='climats.Timekeeper')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('mre_date', models.DateField(blank=True, null=True)),
                ('recent_days', models.IntegerField(default=15, help_text='until files deleted from recent files list.', verbose_name='Days')),
                ('for_whom', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='climats.Timekeeper', verbose_name='entering for')),
            ],
        ),
        migrations.AddField(
            model_name='entry',
            name='recent_files',
            field=models.ForeignKey(blank=True, help_text='Select a recent file to override company, client & case', null=True, on_delete=django.db.models.deletion.CASCADE, to='entries.Matter_use'),
        ),
        migrations.AddField(
            model_name='entry',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='entry',
            name='who',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='climats.Timekeeper', verbose_name='Timekeeper'),
        ),
    ]
