# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0043_member_bi_name_verbose_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='bi_name',
            field=models.TextField(verbose_name='BI nickname'),
        ),
        migrations.AlterField(
            model_name='member',
            name='discharge_date',
            field=models.DateField(default=None, verbose_name='Discharge date', null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='join_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Join date'),
        ),
    ]
