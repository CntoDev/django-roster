# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cnto_notes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='dt',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Note date'),
        ),
    ]
