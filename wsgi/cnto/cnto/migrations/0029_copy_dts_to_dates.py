# -*- coding: utf-8 -*-


from django.db import migrations
from django.utils import timezone
from cnto.models import Absence


def copy_dts_to_dates(apps, schema_editor):
    Member = apps.get_model("cnto", "Member")

    for member in Member.objects.all():
        member.join_date = member.join_dt.date()
        if member.discharge_dt is not None:
            member.discharge_date = member.discharge_dt.date()

        member.save()

    Absence = apps.get_model("cnto", "Absence")

    for absence in Absence.objects.all():
        absence.start_date = absence.start_dt.date()
        absence.end_date = absence.end_dt.date()

        absence.save()


def copy_dates_to_dts(apps, schema_editor):
    Member = apps.get_model("cnto", "Member")

    for member in Member.objects.all():
        member.join_dt = member.join_date
        if member.discharge_date is not None:
            member.discharge_dt = member.discharge_date

        member.save()

    Absence = apps.get_model("cnto", "Absence")

    for absence in Absence.objects.all():
        absence.start_dt = absence.start_date
        absence.end_dt = absence.end_date

        absence.save()


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0028_add_dates_for_dts'),
    ]

    operations = [
        migrations.RunPython(copy_dts_to_dates, copy_dates_to_dts),
    ]
