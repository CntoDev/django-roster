# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0026_eventtype_minimum_required_attendance_minutes'),
    ]

    operations = [
        migrations.CreateModel(
            name='LowAttendanceWarning',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('period_start_dt', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'Period start date')),
                ('period_end_dt', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'Period end date')),
                ('message', models.TextField()),
                ('acknowledged', models.BooleanField(default=False)),
                ('member', models.ForeignKey(to='cnto.Member')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
