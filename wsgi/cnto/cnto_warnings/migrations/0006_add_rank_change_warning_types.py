# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def add_rank_change_warning_types(apps, schema_editor):
    MemberWarningType = apps.get_model("cnto_warnings", "MemberWarningType")
    try:
        MemberWarningType.objects.get(name__iexact="Grunt Demoted")
    except MemberWarningType.DoesNotExist:
        gnt_demoted = MemberWarningType(name="Grunt Demoted")
        gnt_demoted.save()

    try:
        MemberWarningType.objects.get(name__iexact="Reservist Promoted")
    except MemberWarningType.DoesNotExist:
        reservist_promoted = MemberWarningType(name="Reservist Promoted")
        reservist_promoted.save()


def clear_rank_change_warning_types(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('cnto_warnings', '0005_add_contribution_warning_types'),
    ]

    operations = [
        migrations.RunPython(add_rank_change_warning_types, clear_rank_change_warning_types),
    ]
