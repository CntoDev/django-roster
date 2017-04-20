# -*- coding: utf-8 -*-


from django.db import models, migrations


def remove_groups_from_discharged(apps, schema_editor):

    Member = apps.get_model("cnto", "Member")

    for member in Member.objects.all():
        if member.discharged:
            member.member_group = None
            member.save()


def add_groups_to_discharged(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0035_new_ranks'),
    ]

    operations = [
        migrations.RunPython(remove_groups_from_discharged, add_groups_to_discharged),
    ]
