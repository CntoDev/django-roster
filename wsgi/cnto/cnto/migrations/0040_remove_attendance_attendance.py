# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0039_attendance_attendance_minutes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='attendance',
        ),
    ]
