# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0027_member_names_not_unique'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='discharge_date',
            field=models.DateField(default=None, null=True, verbose_name=b'Discharge date'),
        ),
        migrations.AddField(
            model_name='member',
            name='join_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name=b'Join date'),
        ),
        migrations.AlterField(
            model_name='member',
            name='discharge_dt',
            field=models.DateTimeField(default=None, null=True, verbose_name=b'Discharge datetime'),
        ),
        migrations.AlterField(
            model_name='member',
            name='join_dt',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'Join datetime'),
        ),
    ]
