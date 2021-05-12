# -*- coding: utf-8 -*-


from django.db import models, migrations


def add_cpl_rank(apps, schema_editor):

    Rank = apps.get_model("cnto", "Rank")

    try:
        Rank.objects.get(name__iexact="Cpl")
    except Rank.DoesNotExist:
        cpl_rank = Rank(name="Cpl")
        cpl_rank.save()

    try:
        spc_rank = Rank.objects.get(name__iexact="SPC")

        Member = apps.get_model("cnto", "Member")

        members = Member.objects.all()
        for member in members:
            if member.rank == spc_rank:
                member.rank = cpl_rank
                member.save()
    except Rank.DoesNotExist:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('cnto', '0045_add_training_manager_and_set_permissions'),
    ]

    operations = [
        migrations.RunPython(add_cpl_rank),
    ]

