# -*- coding: utf-8 -*-


from django.db import models, migrations


def unassess_bqf_recruits(apps, schema_editor):
    Member = apps.get_model("cnto", "Member")
    Rank = apps.get_model("cnto", "Rank")
    rct_rank = Rank.objects.get(name__iexact="rct")

    for member in Member.objects.all():
        if member.rank == rct_rank:
            member.bqf_assessed = False
            member.save()


def assess_bqf_recruits(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('cnto', '0040_remove_attendance_attendance'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='bqf_assessed',
            field=models.BooleanField(default=True),
        ),
        migrations.RunPython(unassess_bqf_recruits, assess_bqf_recruits),
    ]
