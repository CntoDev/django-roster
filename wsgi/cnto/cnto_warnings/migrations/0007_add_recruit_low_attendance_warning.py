# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def add_recruit_attendance_warning_types(apps, schema_editor):
    MemberWarningType = apps.get_model("cnto_warnings", "MemberWarningType")
    try:
        MemberWarningType.objects.get(name__iexact="Low Attendance (Recruit)")
    except MemberWarningType.DoesNotExist:
        recruit_attendance_warning = MemberWarningType(name="Low Attendance (Recruit)")
        recruit_attendance_warning.save()


def clear_recruit_attendance_warning_types(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('cnto_warnings', '0006_add_rank_change_warning_types'),
    ]

    operations = [
        migrations.RunPython(add_recruit_attendance_warning_types, clear_recruit_attendance_warning_types),
    ]
