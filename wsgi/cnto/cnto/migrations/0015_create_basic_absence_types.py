# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_basic_absence_types(apps, schema_editor):

    AbsenceType = apps.get_model("cnto", "AbsenceType")
    try:
        AbsenceType.objects.get(name__iexact="leave of absence")
    except AbsenceType.DoesNotExist:
        loa_absence_type = AbsenceType(name="Leave of absence")
        loa_absence_type.save()

    try:
        AbsenceType.objects.get(name__iexact="reservist")
    except AbsenceType.DoesNotExist:
        reservist_absence_type = AbsenceType(name="Reservist")
        reservist_absence_type.save()


def delete_basic_absence_types(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0014_absence_data_structures'),
    ]

    operations = [
        migrations.RunPython(create_basic_absence_types, delete_basic_absence_types),
    ]
