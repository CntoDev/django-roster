# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='dt',
            new_name='start_dt',
        ),
        migrations.AddField(
            model_name='event',
            name='end_dt',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 16, 6, 16, 41, 253763)),
            preserve_default=False,
        ),
    ]
