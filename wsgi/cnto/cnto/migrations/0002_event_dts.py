# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils import timezone


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
            field=models.DateTimeField(default=timezone.now),
            preserve_default=False,
        ),
    ]
