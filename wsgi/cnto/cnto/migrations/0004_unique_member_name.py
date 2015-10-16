# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0003_event_duration_minutes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='name',
            field=models.TextField(unique=True),
        ),
    ]
