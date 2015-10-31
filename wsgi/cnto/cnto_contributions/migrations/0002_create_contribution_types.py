# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.utils import timezone
from cnto.models import Absence


def create_contribution_types(apps, schema_editor):
    ContributionType = apps.get_model("cnto_contributions", "ContributionType")

    bronze_contribution = ContributionType(name="Bronze")
    bronze_contribution.save()

    silver_contribution = ContributionType(name="Silver")
    silver_contribution.save()

    gold_contribution = ContributionType(name="Gold")
    gold_contribution.save()


def destroy_contribution_types(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('cnto_contributions', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_contribution_types, destroy_contribution_types),
    ]
