# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0010_non_null_event_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='join_dt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
