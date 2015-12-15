# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0031_membergroup_leader'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventtype',
            old_name='minimum_required_attendance_minutes',
            new_name='minimum_required_attendance_ratio',
        ),
    ]
