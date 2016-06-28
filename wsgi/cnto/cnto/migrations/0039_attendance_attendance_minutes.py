# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def populate_attendance_seconds(apps, schema_editor):

    Attendance = apps.get_model("cnto", "Attendance")

    for attendance in Attendance.objects.all():
        event_duration = ((attendance.event.end_dt - attendance.event.start_dt).total_seconds())
        attendance.attendance_seconds = event_duration * attendance.attendance
        attendance.save()


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0038_rename_rec_to_rct_take2'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='attendance_seconds',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.RunPython(populate_attendance_seconds),
    ]
