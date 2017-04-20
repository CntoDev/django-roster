# -*- coding: utf-8 -*-


from django.db import models, migrations


def rename_rec_to_rct(apps, schema_editor):

    Rank = apps.get_model("cnto", "Rank")

    rank = Rank.objects.get(name__iexact="res")
    rank.name = "Rct"
    rank.save()


def rename_rct_to_rec(apps, schema_editor):

    Rank = apps.get_model("cnto", "Rank")

    rank = Rank.objects.get(name__iexact="rct")
    rank.name = "Rec"
    rank.save()


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0036_no_groups_for_discharged'),
    ]

    operations = [
        migrations.RunPython(rename_rec_to_rct, rename_rct_to_rec),
    ]
