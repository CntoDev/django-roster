# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def deprecate_reservist_type(apps, schema_editor):

    AbsenceType = apps.get_model("cnto", "AbsenceType")
    reservist_type = AbsenceType.objects.get(name__iexact="reservist")
    reservist_type.deprecated = True
    reservist_type.save()


def dedeprecate_reservist_type(apps, schema_editor):

    AbsenceType = apps.get_model("cnto", "AbsenceType")
    reservist_type = AbsenceType.objects.get(name__iexact="reservist")
    reservist_type.deprecated = False
    reservist_type.save()


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0033_auto_20151215_1040'),
    ]

    operations = [
        migrations.AddField(
            model_name='absencetype',
            name='deprecated',
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(deprecate_reservist_type, dedeprecate_reservist_type),
    ]
