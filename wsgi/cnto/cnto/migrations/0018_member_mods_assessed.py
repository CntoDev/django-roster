# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0017_absence_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='mods_assessed',
            field=models.BooleanField(default=True),
        ),
    ]
