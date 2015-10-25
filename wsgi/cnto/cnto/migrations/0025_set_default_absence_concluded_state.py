# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from datetime import datetime
from cnto.models import Absence


def set_default_absence_concluded_state(apps, schema_editor):
    current_dt = datetime.now()

    for absence in Absence.objects.all():
        if absence.start_dt <= current_dt <= absence.end_dt:
            absence.concluded = False
        else:
            absence.concluded = True

        # Without a save, this migration doesn't actually do anything!


def clear_default_absence_concluded_state(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0024_absence_concluded'),
    ]

    operations = [
        migrations.RunPython(set_default_absence_concluded_state, clear_default_absence_concluded_state),
    ]
