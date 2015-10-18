# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0015_create_basic_absence_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
