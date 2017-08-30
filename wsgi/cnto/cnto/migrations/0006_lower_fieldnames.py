# -*- coding: utf-8 -*-


from django.db import migrations, models


def lower_name_values(apps, schema_editor):
    Member = apps.get_model("cnto", "Member")
    for member in Member.objects.all():
        member.name = member.name.lower()
        member.save()

    MemberGroup = apps.get_model("cnto", "MemberGroup")
    for member_group in MemberGroup.objects.all():
        member_group.name = member_group.name.lower()
        member_group.save()

    Rank = apps.get_model("cnto", "Rank")
    for rank in Rank.objects.all():
        rank.name = rank.name.lower()
        rank.save()


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0005_more_unique_fields'),
    ]

    operations = [
        migrations.RunPython(lower_name_values),
    ]
