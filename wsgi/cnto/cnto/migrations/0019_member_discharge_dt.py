# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0018_member_mods_assessed'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='discharge_dt',
            field=models.DateTimeField(default=None, null=True, verbose_name=b'Discharge date'),
        ),
    ]
