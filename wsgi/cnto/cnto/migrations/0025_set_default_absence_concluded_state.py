# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils import timezone
from cnto.models import Absence


def set_default_absence_concluded_state(apps, schema_editor):
    current_dt = timezone.now()

    for absence in Absence.objects.all():
        if absence.start_dt <= current_dt <= absence.end_dt:
            absence.concluded = False
        else:
            absence.concluded = True

        # Without a save, this migration doesn't actually do anything!
    print "Done"


def clear_default_absence_concluded_state(apps, schema_editor):
    pass


def migrate_absence_data_to_date(apps, schema_editor):
    for absence in Absence.objects.all():
        absence.start_date = absence.start_dt.date()
        absence.end_date = absence.end_dt.date()
        absence.save()


def unmigrate_absence_data_from_date(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0024_absence_concluded'),
    ]

    operations = [
        migrations.AddField(
            model_name='absence',
            name='start_date',
            field=models.DateField(null=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='absence',
            name='end_date',
            field=models.DateField(null=False),
            preserve_default=False,
        ),
        migrations.RunPython(migrate_absence_data_to_date, unmigrate_absence_data_from_date),
        migrations.RemoveField(
            model_name='absence',
            name='start_dt',
        ),
        migrations.RemoveField(
            model_name='absence',
            name='end_dt',
        ),

        migrations.RunPython(set_default_absence_concluded_state, clear_default_absence_concluded_state),
    ]
